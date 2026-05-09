using UnrealBuildTool;
using System.Collections.Generic;

public class SmartFactory_CameraModuleEditorTarget : TargetRules
{
	public SmartFactory_CameraModuleEditorTarget(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Editor;
		bOverrideBuildEnvironment = true;
		DefaultBuildSettings = BuildSettingsVersion.V5;
		IncludeOrderVersion = EngineIncludeOrderVersion.Unreal5_5;
		ExtraModuleNames.Add("SmartFactory_CameraModule");
	}
}
