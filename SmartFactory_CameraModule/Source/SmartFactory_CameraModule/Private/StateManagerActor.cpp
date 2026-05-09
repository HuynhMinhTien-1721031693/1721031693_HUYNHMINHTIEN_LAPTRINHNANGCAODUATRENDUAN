#include "StateManagerActor.h"

#include "Engine/DataTable.h"
#include "HttpModule.h"
#include "Interfaces/IHttpRequest.h"
#include "Interfaces/IHttpResponse.h"
#include "Json.h"
#include "TimerManager.h"

namespace
{
	static FString TrimStatus(const FString& S)
	{
		FString T = S;
		T.TrimStartAndEndInline();
		return T.ToLower();
	}
}

AStateManagerActor::AStateManagerActor()
{
	PrimaryActorTick.bCanEverTick = false;
	bReplicates = false;

	InputComponent = CreateDefaultSubobject<UInputComponent>(TEXT("StateManagerInput"));
}

void AStateManagerActor::BeginPlay()
{
	Super::BeginPlay();

	if (APlayerController* PC = GetWorld() ? GetWorld()->GetFirstPlayerController() : nullptr)
	{
		EnableInput(PC);
	}

	if (InputComponent)
	{
		BindDebugKeys(InputComponent);
	}

	if (bUseHttpPolling)
	{
		StartPolling();
	}
}

void AStateManagerActor::BindDebugKeys(UInputComponent* IC)
{
	if (!IC)
	{
		return;
	}

	IC->BindKey(EKeys::One, IE_Pressed, this, &AStateManagerActor::OnDebugKey_Idle);
	IC->BindKey(EKeys::Two, IE_Pressed, this, &AStateManagerActor::OnDebugKey_Scanning);
	IC->BindKey(EKeys::Three, IE_Pressed, this, &AStateManagerActor::OnDebugKey_DetectedOK);
	IC->BindKey(EKeys::Four, IE_Pressed, this, &AStateManagerActor::OnDebugKey_DetectedWarning);
	IC->BindKey(EKeys::Five, IE_Pressed, this, &AStateManagerActor::OnDebugKey_Error);
	IC->BindKey(EKeys::Six, IE_Pressed, this, &AStateManagerActor::OnDebugKey_FireAlert);
}

void AStateManagerActor::OnDebugKey_Idle()
{
	ClearReturnToIdleTimer();
	SetModuleState(EModuleState::Idle);
}

void AStateManagerActor::OnDebugKey_Scanning()
{
	ClearReturnToIdleTimer();
	SetModuleState(EModuleState::Scanning);
}

void AStateManagerActor::OnDebugKey_DetectedOK()
{
	ClearReturnToIdleTimer();
	SetModuleState(EModuleState::Detected_OK);
}

void AStateManagerActor::OnDebugKey_DetectedWarning()
{
	ClearReturnToIdleTimer();
	SetModuleState(EModuleState::Detected_Warning);
}

void AStateManagerActor::OnDebugKey_Error()
{
	ClearReturnToIdleTimer();
	SetModuleState(EModuleState::Error);
}

void AStateManagerActor::OnDebugKey_FireAlert()
{
	ClearReturnToIdleTimer();
	SetModuleState(EModuleState::Fire_Alert);
}

void AStateManagerActor::SetModuleState(EModuleState NewState, bool bBroadcast)
{
	if (CurrentState == NewState && !bBroadcast)
	{
		return;
	}

	CurrentState = NewState;

	if (bBroadcast)
	{
		OnStateChanged.Broadcast(CurrentState);
	}
}

void AStateManagerActor::StartPolling()
{
	StopPolling();

	if (!GetWorld())
	{
		return;
	}

	if (PollIntervalSeconds > 0.f)
	{
		GetWorld()->GetTimerManager().SetTimer(
			PollTimerHandle,
			this,
			&AStateManagerActor::OnPollTimer,
			PollIntervalSeconds,
			true);
	}

	OnPollTimer();
}

void AStateManagerActor::StopPolling()
{
	if (GetWorld())
	{
		GetWorld()->GetTimerManager().ClearTimer(PollTimerHandle);
	}
}

void AStateManagerActor::ClearReturnToIdleTimer()
{
	if (GetWorld())
	{
		GetWorld()->GetTimerManager().ClearTimer(ReturnToIdleTimerHandle);
	}
}

void AStateManagerActor::OnPollTimer()
{
	if (!bUseHttpPolling)
	{
		TryFallbackDataTableRow();
		return;
	}

	if (bPollRequestInFlight)
	{
		return;
	}

	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Req = FHttpModule::Get().CreateRequest();
	const FString Url = HttpBaseUrl.EndsWith(TEXT("/")) ? (HttpBaseUrl + TEXT("current")) : (HttpBaseUrl + TEXT("/current"));
	Req->SetURL(Url);
	Req->SetVerb(TEXT("GET"));
	Req->SetTimeout(3.f);
	Req->OnProcessRequestComplete().BindUObject(this, &AStateManagerActor::Http_OnComplete);

	bPollRequestInFlight = true;
	Req->ProcessRequest();
}

void AStateManagerActor::Http_OnComplete(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bConnectedSuccessfully)
{
	(void)Request;
	bPollRequestInFlight = false;

	const bool bOk = bConnectedSuccessfully && Response.IsValid() && Response->GetResponseCode() == 200;
	if (!bOk)
	{
		if (bFallbackToDataTableOnHttpFailure)
		{
			TryFallbackDataTableRow();
		}
		return;
	}

	const FString Body = Response->GetContentAsString();
	FCurrentScanObject Payload;
	if (!JsonToPayload(Body, Payload))
	{
		if (bFallbackToDataTableOnHttpFailure)
		{
			TryFallbackDataTableRow();
		}
		return;
	}

	ProcessPayload(Payload, true);
}

bool AStateManagerActor::JsonToPayload(const FString& JsonString, FCurrentScanObject& OutPayload)
{
	TSharedPtr<FJsonObject> Root;
	const TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(JsonString);
	if (!FJsonSerializer::Deserialize(Reader, Root) || !Root.IsValid())
	{
		return false;
	}

	auto GetStr = [&Root](const TCHAR* A, const TCHAR* B) -> FString
	{
		FString V;
		if (Root->TryGetStringField(A, V))
		{
			return V;
		}
		if (B && Root->TryGetStringField(B, V))
		{
			return V;
		}
		return FString();
	};

	OutPayload.ObjectID = GetStr(TEXT("object_id"), TEXT("ObjectID"));
	OutPayload.ObjectType = GetStr(TEXT("object_type"), TEXT("ObjectType"));
	OutPayload.Status = TrimStatus(GetStr(TEXT("status"), nullptr));

	double W = 0.0;
	if (Root->TryGetNumberField(TEXT("weight_kg"), W))
	{
		OutPayload.WeightKg = static_cast<float>(W);
	}
	else if (Root->TryGetNumberField(TEXT("Weight"), W))
	{
		OutPayload.WeightKg = static_cast<float>(W);
	}

	double Tc = 0.0;
	if (Root->TryGetNumberField(TEXT("temperature_c"), Tc))
	{
		OutPayload.TemperatureC = static_cast<float>(Tc);
	}
	else if (Root->TryGetNumberField(TEXT("TemperatureC"), Tc))
	{
		OutPayload.TemperatureC = static_cast<float>(Tc);
	}

	OutPayload.bHasAnomaly = false;
	FString AnomalyStr;
	if (Root->TryGetStringField(TEXT("anomaly"), AnomalyStr))
	{
		OutPayload.bHasAnomaly = !AnomalyStr.IsEmpty();
	}

	return true;
}

EModuleState AStateManagerActor::ClassifyPayload(const FCurrentScanObject& Payload, float FireThreshold)
{
	if (Payload.TemperatureC > FireThreshold)
	{
		return EModuleState::Fire_Alert;
	}

	const FString S = TrimStatus(Payload.Status);
	if (S == TEXT("ok"))
	{
		return EModuleState::Detected_OK;
	}
	if (S == TEXT("warning"))
	{
		return EModuleState::Detected_Warning;
	}
	if (S == TEXT("error"))
	{
		return EModuleState::Error;
	}

	return EModuleState::Detected_Warning;
}

void AStateManagerActor::ProcessPayload(const FCurrentScanObject& Payload, bool bFromHttp)
{
	(void)bFromHttp;

	ClearReturnToIdleTimer();

	CurrentObject = Payload;

	SetModuleState(EModuleState::Scanning);
	SetModuleState(ClassifyPayload(CurrentObject, FireAlertTemperatureC));

	ScheduleReturnToIdle();
}

void AStateManagerActor::ScheduleReturnToIdle()
{
	if (!GetWorld() || IdleReturnDelaySeconds <= 0.f)
	{
		return;
	}

	GetWorld()->GetTimerManager().SetTimer(
		ReturnToIdleTimerHandle,
		FTimerDelegate::CreateLambda([this]()
		{
			SetModuleState(EModuleState::Idle);
		}),
		IdleReturnDelaySeconds,
		false);
}

void AStateManagerActor::TryFallbackDataTableRow()
{
	if (!FallbackDataTable)
	{
		return;
	}

	const TArray<FName> RowNames = FallbackDataTable->GetRowNames();
	if (RowNames.Num() == 0)
	{
		return;
	}

	if (DataTableRowIndex >= RowNames.Num())
	{
		if (!bLoopDataTableRows)
		{
			return;
		}
		DataTableRowIndex = 0;
	}

	const FName RowName = RowNames[DataTableRowIndex];
	const FScanEventTableRow* Row = FallbackDataTable->FindRow<FScanEventTableRow>(RowName, TEXT("StateManagerActor::TryFallbackDataTableRow"));
	if (!Row)
	{
		DataTableRowIndex++;
		TryFallbackDataTableRow();
		return;
	}

	FCurrentScanObject P;
	P.ObjectID = Row->ObjectID;
	P.ObjectType = Row->ObjectType;
	P.WeightKg = Row->WeightKg;
	P.TemperatureC = Row->TemperatureC;
	P.Status = TrimStatus(Row->Status);
	P.bHasAnomaly = !Row->Anomaly.IsEmpty();

	ProcessPayload(P, false);

	DataTableRowIndex++;
}
