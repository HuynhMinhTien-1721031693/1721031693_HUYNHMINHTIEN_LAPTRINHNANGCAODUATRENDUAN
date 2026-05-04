#pragma once

#include "CoreMinimal.h"
#include "Engine/DataTable.h"
#include "ScanningDataTypes.generated.h"

UENUM(BlueprintType)
enum class EModuleState : uint8
{
	Idle UMETA(DisplayName = "Idle"),
	Scanning UMETA(DisplayName = "Scanning"),
	Detected UMETA(DisplayName = "Detected"),
	Error UMETA(DisplayName = "Error")
};

USTRUCT(BlueprintType)
struct FObjectData : public FTableRowBase
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Object Data")
	FName ObjectID = NAME_None;

	// FName is chosen for fast comparisons and compact storage.
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Object Data")
	FName ObjectType = NAME_None;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Object Data")
	float ScanDuration = 0.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Object Data")
	float Weight = 0.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Object Data")
	bool IsValid = false;
};
