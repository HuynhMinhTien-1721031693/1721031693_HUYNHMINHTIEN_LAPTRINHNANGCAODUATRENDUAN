#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "SmartFactory_CameraModule.h"
#include "ScanningDataTypes.h"
#include "StateManagerActor.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnModuleStateChanged, EModuleState, NewState);

UCLASS(Blueprintable, BlueprintType)
class SMARTFACTORY_CAMERAMODULE_API AStateManagerActor : public AActor
{
	GENERATED_BODY()

public:
	AStateManagerActor();

	virtual void BeginPlay() override;

	/** Fires when `CurrentState` changes (HTTP, DataTable, or debug keys). */
	UPROPERTY(BlueprintAssignable, Category = "State|Events")
	FOnModuleStateChanged OnStateChanged;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "State")
	EModuleState CurrentState = EModuleState::Idle;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "State")
	FCurrentScanObject CurrentObject;

	/** GET http://host:port/current */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "State|HTTP")
	FString HttpBaseUrl = TEXT("http://127.0.0.1:8080");

	/** Seconds between automatic polls. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "State|HTTP", meta = (ClampMin = "0.1"))
	float PollIntervalSeconds = 3.f;

	/** After a classified result, return to Idle this many seconds later. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "State|HTTP", meta = (ClampMin = "0.0"))
	float IdleReturnDelaySeconds = 2.5f;

	/** If true, use FHttpModule; if false, use DataTable / mock only. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "State|HTTP")
	bool bUseHttpPolling = true;

	/** If HTTP request fails, try one DataTable row (when DataTable is set). */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "State|HTTP")
	bool bFallbackToDataTableOnHttpFailure = true;

	/** Optional. Row struct must be FScanEventTableRow. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "State|DataTable")
	UDataTable* FallbackDataTable = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "State|DataTable")
	bool bLoopDataTableRows = true;

	/** Thermal override threshold (°C): above this => Fire_Alert. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "State|Rules")
	float FireAlertTemperatureC = 55.f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "State|Rules")
	float WarningTemperatureC = 40.f;

	UFUNCTION(BlueprintCallable, Category = "State")
	void SetModuleState(EModuleState NewState, bool bBroadcast = true);

	UFUNCTION(BlueprintCallable, Category = "State")
	void StartPolling();

	UFUNCTION(BlueprintCallable, Category = "State")
	void StopPolling();

protected:
	void BindDebugKeys(UInputComponent* IC);
	void OnDebugKey_Idle();
	void OnDebugKey_Scanning();
	void OnDebugKey_DetectedOK();
	void OnDebugKey_DetectedWarning();
	void OnDebugKey_Error();
	void OnDebugKey_FireAlert();

	void OnPollTimer();
	void ScheduleReturnToIdle();
	void ClearReturnToIdleTimer();

	void ProcessPayload(const FCurrentScanObject& Payload, bool bFromHttp);

	static bool JsonToPayload(const FString& JsonString, FCurrentScanObject& OutPayload);
	static EModuleState ClassifyPayload(const FCurrentScanObject& Payload, float FireThreshold);

	void Http_OnComplete(class FHttpRequestPtr Request, class FHttpResponsePtr Response, bool bConnectedSuccessfully);
	void TryFallbackDataTableRow();

	UPROPERTY()
	int32 DataTableRowIndex = 0;

	FTimerHandle PollTimerHandle;
	FTimerHandle ReturnToIdleTimerHandle;

	bool bPollRequestInFlight = false;
};
