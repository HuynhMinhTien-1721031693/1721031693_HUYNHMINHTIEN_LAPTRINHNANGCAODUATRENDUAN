using UnrealBuildTool;
using System.Collections.Generic;

public class SmartFactory_CameraModuleTarget : TargetRules
{
	public SmartFactory_CameraModuleTarget(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Game;
		DefaultBuildSettings = BuildSettingsVersion.V5;
		IncludeOrderVersion = EngineIncludeOrderVersion.Unreal5_5;
		ExtraModuleNames.Add("SmartFactory_CameraModule");
	}
}
