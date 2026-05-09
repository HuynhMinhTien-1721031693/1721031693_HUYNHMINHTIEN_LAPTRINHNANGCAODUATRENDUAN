#pragma once

#include "CoreMinimal.h"
#include "Engine/DataTable.h"
#include "ScanningDataTypes.generated.h"

UENUM(BlueprintType)
enum class EModuleState : uint8
{
	Idle UMETA(DisplayName = "Idle"),
	Scanning UMETA(DisplayName = "Scanning"),
	Detected_OK UMETA(DisplayName = "Detected OK"),
	Detected_Warning UMETA(DisplayName = "Detected Warning"),
	Error UMETA(DisplayName = "Error"),
	Fire_Alert UMETA(DisplayName = "Fire Alert")
};

UENUM(BlueprintType)
enum class EScanState : uint8
{
	Idle UMETA(DisplayName = "Idle"),
	ConveyorRunning UMETA(DisplayName = "Conveyor Running"),
	ObjectDetected UMETA(DisplayName = "Object Detected"),
	Scanning UMETA(DisplayName = "Scanning"),
	Classified UMETA(DisplayName = "Classified"),
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

USTRUCT(BlueprintType)
struct FScanObjectRow : public FTableRowBase
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Scan Object")
	FName ObjectID = NAME_None;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Scan Object")
	FName ObjectType = NAME_None;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Scan Object")
	float Weight = 0.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Scan Object")
	bool IsDefective = false;

	// ISO-8601 string from mock generator. Keep string for direct JSON/CSV compatibility.
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Scan Object")
	FString ScanTimestamp;
};

USTRUCT(BlueprintType)
struct FScannerConfig
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Scanner")
	float ScanDurationSeconds = 0.5f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Scanner")
	float ConveyorSpeedCmPerSec = 120.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Scanner")
	float SpawnIntervalSeconds = 1.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Scanner")
	bool bAutoCycle = true;
};

/** Payload from HTTP GET /current (matches camera_server.py canonical JSON). */
USTRUCT(BlueprintType)
struct FCurrentScanObject
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Scan")
	FString ObjectID;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Scan")
	FString ObjectType;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Scan")
	float WeightKg = 0.f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Scan")
	float TemperatureC = 0.f;

	/** Lowercase ok | warning | error from server. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Scan")
	FString Status;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Scan")
	bool bHasAnomaly = false;
};

/** Row type for optional DataTable fallback when HTTP is disabled or fails. */
USTRUCT(BlueprintType)
struct FScanEventTableRow : public FTableRowBase
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Scan")
	FString ObjectID;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Scan")
	FString ObjectType;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Scan")
	float WeightKg = 0.f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Scan")
	float TemperatureC = 0.f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Scan")
	FString Status;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Scan")
	FString Anomaly;
};
