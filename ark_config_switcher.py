import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import json
import string
from pathlib import Path

# Configuration file location - AppData/Roaming
APPDATA_FOLDER = os.path.join(os.getenv('APPDATA'), 'ark_config_switcher')
CONFIG_FILE = os.path.join(APPDATA_FOLDER, 'settings.json')

# Ensure appdata folder exists
os.makedirs(APPDATA_FOLDER, exist_ok=True)

# Dark mode colors
DARK_BG = "#1e1e1e"
DARK_FG = "#e0e0e0"
DARK_HEADER = "#252526"
ACCENT_BLUE = "#0d7377"
ACCENT_GREEN = "#2d6a4f"
ACCENT_ORANGE = "#d97706"
BUTTON_BG = "#2d2d30"
BUTTON_HOVER = "#3e3e42"
INPUT_BG = "#2d2d30"
INPUT_FG = "#cccccc"


class ConfigManager:
    
    CONFIGS = {
        "DEFAULT": """[DeviceProfiles]
+DeviceProfileNameAndTypes=Windows,Windows
+DeviceProfileNameAndTypes=WindowsNoEditor,WindowsNoEditor
+DeviceProfileNameAndTypes=WindowsServer,WindowsServer
+DeviceProfileNameAndTypes=IOS,IOS
+DeviceProfileNameAndTypes=iPad2,IOS
+DeviceProfileNameAndTypes=iPad3,IOS
+DeviceProfileNameAndTypes=iPad4,IOS
+DeviceProfileNameAndTypes=iPadAir,IOS
+DeviceProfileNameAndTypes=iPadMini,IOS
+DeviceProfileNameAndTypes=iPadMini2,IOS
+DeviceProfileNameAndTypes=iPhone4,IOS
+DeviceProfileNameAndTypes=iPhone4S,IOS
+DeviceProfileNameAndTypes=iPhone5,IOS
+DeviceProfileNameAndTypes=iPhone5S,IOS
+DeviceProfileNameAndTypes=iPodTouch5,IOS
+DeviceProfileNameAndTypes=iPhone6,IOS
+DeviceProfileNameAndTypes=iPhone6Plus,IOS
+DeviceProfileNameAndTypes=Android,Android
+DeviceProfileNameAndTypes=PS4,PS4
+DeviceProfileNameAndTypes=XboxOne,XboxOne
+DeviceProfileNameAndTypes=HTML5,HTML5
+DeviceProfileNameAndTypes=Mac,Mac
+DeviceProfileNameAndTypes=MacNoEditor,MacNoEditor
+DeviceProfileNameAndTypes=MacServer,MacServer
+DeviceProfileNameAndTypes=WinRT,WinRT
+DeviceProfileNameAndTypes=Linux,Linux
+DeviceProfileNameAndTypes=LinuxNoEditor,LinuxNoEditor
+DeviceProfileNameAndTypes=LinuxServer,LinuxServer

[Windows DeviceProfile]
DeviceType=Windows
BaseProfileName=

[WindowsNoEditor DeviceProfile]
DeviceType=WindowsNoEditor
BaseProfileName=Windows

[WindowsServer DeviceProfile]
DeviceType=WindowsServer
BaseProfileName=Windows

[IOS DeviceProfile]
DeviceType=IOS
BaseProfileName=
+CVars=r.BloomQuality=0
+CVars=r.DepthOfFieldQuality=0
+CVars=r.LightShaftQuality=0
+CVars=r.RefractionQuality=0

[iPad2 DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.RenderTargetSwitchWorkaround=1

[iPad3 DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.RenderTargetSwitchWorkaround=1

[iPad4 DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.RenderTargetSwitchWorkaround=1

[iPadAir DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.BloomQuality=1

[iPadMini DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.RenderTargetSwitchWorkaround=1

[iPadMini2 DeviceProfile]
DeviceType=IOS
BaseProfileName=iPadAir

[iPhone4 DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.RenderTargetSwitchWorkaround=1

[iPhone4S DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.RenderTargetSwitchWorkaround=1

[iPhone5 DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.RenderTargetSwitchWorkaround=1

[iPhone5S DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.MobileContentScaleFactor=2
+CVars=r.BloomQuality=1
+CVars=r.DepthOfFieldQuality=1
+CVars=r.LightShaftQuality=1

[iPodTouch5 DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.RenderTargetSwitchWorkaround=1

[iPhone6 DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.MobileContentScaleFactor=0
+CVars=r.BloomQuality=1
+CVars=r.DepthOfFieldQuality=1
+CVars=r.LightShaftQuality=1

[iPhone6Plus DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.MobileContentScaleFactor=0
+CVars=r.BloomQuality=1
+CVars=r.DepthOfFieldQuality=1
+CVars=r.LightShaftQuality=1

[Android DeviceProfile]
DeviceType=Android
BaseProfileName=
+CVars=r.MobileContentScaleFactor=1
+CVars=r.BloomQuality=0
+CVars=r.DepthOfFieldQuality=0
+CVars=r.LightShaftQuality=0
+CVars=r.RefractionQuality=0

[Android_Low DeviceProfile]
DeviceType=Android
BaseProfileName=Android
+CVars=r.MobileContentScaleFactor=0.5

[Android_Mid DeviceProfile]
DeviceType=Android
BaseProfileName=Android
+CVars=r.BloomQuality=1
+CVars=r.MobileContentScaleFactor=0.8

[Android_High DeviceProfile]
DeviceType=Android
BaseProfileName=Android
+CVars=r.BloomQuality=1
+CVars=r.DepthOfFieldQuality=1
+CVars=r.LightShaftQuality=1
+CVars=r.MobileContentScaleFactor=1.0

[Android_Unrecognized DeviceProfile]
DeviceType=Android
BaseProfileName=Android_Mid

[Android_Adreno320 DeviceProfile]
DeviceType=Android
BaseProfileName=Android_Mid

;This offset needs to be set for the mosaic fallback to work on Galaxy S4 (SAMSUNG-IGH-I337)
;+CVars=r.DemosaicVposOffset=0.5

[Android_Adreno330 DeviceProfile]
DeviceType=Android
BaseProfileName=Android_High

[Android_Adreno330_Ver53 DeviceProfile]
DeviceType=Android
BaseProfileName=Android_Adreno330
+CVars=r.DisjointTimerQueries=1

[PS4 DeviceProfile]
DeviceType=PS4
BaseProfileName=

[XboxOne DeviceProfile]
DeviceType=XboxOne
BaseProfileName=
; we output 10:10:10, not 8:8:8 so we don't need color quantization
+CVars=r.TonemapperQuality=0
; For SSAO we rely on TemporalAA (with a randomized sample pattern over time) so we can use less samples
+CVars=r.AmbientOcclusionSampleSetQuality=0
; less passes, and no upsampling as even upsampling costs some performance
+CVars=r.AmbientOcclusionLevels=1
; larger radius to compensate for fewer passes
+CVars=r.AmbientOcclusionRadiusScale=2


[HTML5 DeviceProfile]
DeviceType=HTML5
BaseProfileName=
+CVars=r.RefractionQuality=0

[Mac DeviceProfile]
DeviceType=Mac
BaseProfileName=

[MacNoEditor DeviceProfile]
DeviceType=MacNoEditor
BaseProfileName=Mac

[MacServer DeviceProfile]
DeviceType=MacServer
BaseProfileName=Mac

[WinRT DeviceProfile]
DeviceType=WinRT
BaseProfileName=

[Linux DeviceProfile]
DeviceType=Linux
BaseProfileName=
MeshLODSettings=
TextureLODSettings=

[LinuxNoEditor DeviceProfile]
DeviceType=LinuxNoEditor
BaseProfileName=Linux
MeshLODSettings=
TextureLODSettings=

[LinuxServer DeviceProfile]
DeviceType=LinuxServer
BaseProfileName=Linux
MeshLODSettings=
TextureLODSettings=
""",
        "PVP": """[DeviceProfiles]
+DeviceProfileNameAndTypes=Windows,Windows
+DeviceProfileNameAndTypes=WindowsNoEditor,WindowsNoEditor
+DeviceProfileNameAndTypes=WindowsServer,WindowsServer
+DeviceProfileNameAndTypes=IOS,IOS
+DeviceProfileNameAndTypes=iPad2,IOS
+DeviceProfileNameAndTypes=iPad3,IOS
+DeviceProfileNameAndTypes=iPad4,IOS
+DeviceProfileNameAndTypes=iPadAir,IOS
+DeviceProfileNameAndTypes=iPadMini,IOS
+DeviceProfileNameAndTypes=iPadMini2,IOS
+DeviceProfileNameAndTypes=iPhone4,IOS
+DeviceProfileNameAndTypes=iPhone4S,IOS
+DeviceProfileNameAndTypes=iPhone5,IOS
+DeviceProfileNameAndTypes=iPhone5S,IOS
+DeviceProfileNameAndTypes=iPodTouch5,IOS
+DeviceProfileNameAndTypes=iPhone6,IOS
+DeviceProfileNameAndTypes=iPhone6Plus,IOS
+DeviceProfileNameAndTypes=Android,Android
+DeviceProfileNameAndTypes=PS4,PS4
+DeviceProfileNameAndTypes=XboxOne,XboxOne
+DeviceProfileNameAndTypes=HTML5,HTML5
+DeviceProfileNameAndTypes=Mac,Mac
+DeviceProfileNameAndTypes=MacNoEditor,MacNoEditor
+DeviceProfileNameAndTypes=MacServer,MacServer
+DeviceProfileNameAndTypes=WinRT,WinRT
+DeviceProfileNameAndTypes=Linux,Linux
+DeviceProfileNameAndTypes=LinuxNoEditor,LinuxNoEditor
+DeviceProfileNameAndTypes=LinuxServer,LinuxServer

[Windows DeviceProfile]
DeviceType=Windows
BaseProfileName=
+CVars=foliage.UseOcclusionType=0
+CVars=ShowFloatingDamageText=True
+CVars=FogDensity=0.0
+CVars=FrameRateCap=144
+CVars=FrameRateMinimum=144
+CVars=MaxES2PixelShaderAdditiveComplexityCount=45
+CVars=MaxPixelShaderAdditiveComplexityCount=128
+CVars=MaxSmoothedFrameRate=144
+CVars=MinDesiredFrameRate=70
+CVars=MinSmoothedFrameRate=5
+CVars=NearClipPlane=12.0
+CVars=ShowFlag.AmbientOcclusion=0
+CVars=ShowFlag.AntiAliasing=0
+CVars=ShowFlag.Atmosphere=0
+CVars=ShowFlag.AtmosphericFog=0
+CVars=ShowFlag.AudioRadius=0
+CVars=ShowFlag.BSP=0
+CVars=ShowFlag.BSPSplit=0
+CVars=ShowFlag.BSPTriangles=0
+CVars=ShowFlag.BillboardSprites=0
+CVars=ShowFlag.Brushes=0
+CVars=ShowFlag.BuilderBrush=0
+CVars=ShowFlag.CameraAspectRatioBars=0
+CVars=ShowFlag.CameraFrustums=0
+CVars=ShowFlag.CameraImperfections=0
+CVars=ShowFlag.CameraInterpolation=0
+CVars=ShowFlag.CameraSafeFrames=0
+CVars=ShowFlag.ColorGrading=0
+CVars=ShowFlag.CompositeEditorPrimitives=0
+CVars=ShowFlag.Constraints=0
+CVars=ShowFlag.Cover=0
+CVars=ShowFlag.Decals=0
+CVars=ShowFlag.DeferredLighting=0
+CVars=ShowFlag.DepthOfField=0
+CVars=ShowFlag.Diffuse=0
+CVars=ShowFlag.DirectLighting=0
+CVars=ShowFlag.DirectionalLights=0
+CVars=ShowFlag.DistanceCulledPrimitives=0
+CVars=ShowFlag.DistanceFieldAO=0
+CVars=ShowFlag.DynamicShadows=0
+CVars=ShowFlag.Editor=0
+CVars=ShowFlag.EyeAdaptation=0
+CVars=ShowFlag.Fog=1
+CVars=ShowFlag.Game=0
+CVars=ShowFlag.LOD=0
+CVars=ShowFlag.Landscape=0
+CVars=ShowFlag.LargeVertices=0
+CVars=ShowFlag.LensFlares=0
+CVars=ShowFlag.LevelColoration=0
+CVars=ShowFlag.LightComplexity=0
+CVars=ShowFlag.LightInfluences=0
+CVars=ShowFlag.LightMapDensity=0
+CVars=ShowFlag.LightRadius=0
+CVars=ShowFlag.LightShafts=0
+CVars=ShowFlag.Lighting=0
+CVars=ShowFlag.LpvLightingOnly=0
+CVars=ShowFlag.Materials=0
+CVars=ShowFlag.MeshEdges=0
+CVars=ShowFlag.MotionBlur=0
+CVars=ShowFlag.OnScreenDebug=0
+CVars=ShowFlag.OverrideDiffuseAndSpecular=0
+CVars=ShowFlag.Paper2DSprites=0
+CVars=ShowFlag.Particles=0
+CVars=ShowFlag.Pivot=0
+CVars=ShowFlag.PointLights=0
+CVars=ShowFlag.PostProcessMaterial=0
+CVars=ShowFlag.PostProcessing=0
+CVars=ShowFlag.PrecomputedVisibility=0
+CVars=ShowFlag.PreviewShadowsIndicator=0
+CVars=ShowFlag.ReflectionEnvironment=0
+CVars=ShowFlag.ReflectionOverride=0
+CVars=ShowFlag.Refraction=0
+CVars=ShowFlag.SelectionOutline=0
+CVars=ShowFlag.ShaderComplexity=0
+CVars=ShowFlag.ShadowFrustums=0
+CVars=ShowFlag.ShadowsFromEditorHiddenActors=0
+CVars=ShowFlag.SkeletalMeshes=0
+CVars=ShowFlag.SkyLighting=0
+CVars=ShowFlag.Snap=0
+CVars=ShowFlag.Specular=0
+CVars=ShowFlag.SpotLights=0
+CVars=ShowFlag.StaticMeshes=0
+CVars=ShowFlag.StationaryLightOverlap=0
+CVars=ShowFlag.StereoRendering=0
+CVars=ShowFlag.SubsurfaceScattering=0
+CVars=ShowFlag.TemporalAA=0
+CVars=ShowFlag.Tessellation=0
+CVars=ShowFlag.TestImage=0
+CVars=ShowFlag.TextRender=0
+CVars=ShowFlag.TexturedLightProfiles=0
+CVars=ShowFlag.Tonemapper=0
+CVars=ShowFlag.Translucency=0
+CVars=ShowFlag.VectorFields=0
+CVars=ShowFlag.VertexColors=0
+CVars=ShowFlag.Vignette=0
+CVars=ShowFlag.VisualizeAdaptiveDOF=0
+CVars=ShowFlag.VisualizeBuffer=0
+CVars=ShowFlag.VisualizeDOF=0
+CVars=ShowFlag.VisualizeDistanceFieldAO=0
+CVars=ShowFlag.VisualizeHDR=0
+CVars=ShowFlag.VisualizeLPV=0
+CVars=ShowFlag.VisualizeLightCulling=0
+CVars=ShowFlag.VisualizeMotionBlur=0
+CVars=ShowFlag.VisualizeOutOfBoundsPixels=0
+CVars=ShowFlag.VisualizeSSR=0
+CVars=ShowFlag.VisualizeSenses=0
+CVars=ShowFlag.VolumeLightingSamples=0
+CVars=ShowFlag.Wireframe=0
+CVars=SmoothedFrameRateRange=(LowerBound=(Type="ERangeBoundTypes::Inclusive",Value=60),UpperBound=(Type="ERangeBoundTypes::Exclusive",Value=70))
+CVars=TEXTUREGROUP_Character=(MinLODSize=1,MaxLODSize=4,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_CharacterNormalMap=(MinLODSize=1,MaxLODSize=4,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_CharacterSpecular=(MinLODSize=1,MaxLODSize=4,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_Cinematic=(MinLODSize=1,MaxLODSize=128,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_Effects=(MinLODSize=1,MaxLODSize=128,LODBias=0,MinMagFilter=linear,MipFilter=point)
+CVars=TEXTUREGROUP_EffectsNotFiltered=(MinLODSize=1,MaxLODSize=128,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_Lightmap=(MinLODSize=1,MaxLODSize=8,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_MobileFlattened=(MinLODSize=1,MaxLODSize=2,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_RenderTarget=(MinLODSize=1,MaxLODSize=128,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_Shadowmap=(MinLODSize=1,MaxLODSize=2,LODBias=0,MinMagFilter=aniso,MipFilter=point,NumStreamedMips=3)
+CVars=TEXTUREGROUP_Skybox=(MinLODSize=1,MaxLODSize=256,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_Terrain_Heightmap=(MinLODSize=1,MaxLODSize=2,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_Terrain_Weightmap=(MinLODSize=1,MaxLODSize=2,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_UI=(MinLODSize=1,MaxLODSize=256,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_Vehicle=(MinLODSize=1,MaxLODSize=256,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_VehicleNormalMap=(MinLODSize=1,MaxLODSize=256,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_VehicleSpecular=(MinLODSize=1,MaxLODSize=256,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_Weapon=(MinLODSize=1,MaxLODSize=64,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_WeaponNormalMap=(MinLODSize=1,MaxLODSize=64,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_WeaponSpecular=(MinLODSize=1,MaxLODSize=64,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_World=(MinLODSize=1,MaxLODSize=2,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_WorldNormalMap=(MinLODSize=1,MaxLODSize=2,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_WorldSpecular=(MinLODSize=1,MaxLODSize=2,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=bDisablePhysXHardwareSupport=True
+CVars=bFirstRun=False
+CVars=bSmoothFrameRate=true
+CVars=r.AOTrimOldRecordsFraction=0
+CVars=r.AmbientOcclusionLevels=0
+CVars=r.Atmosphere=0
+CVars=r.BloomQuality=0
+CVars=r.ClearWithExcludeRects=0
+CVars=r.CompileShadersForDevelopment=0
+CVars=r.CustomDepth=0
+CVars=r.DefaultFeature.AmbientOcclusion=False
+CVars=r.DefaultFeature.AntiAliasing=0
+CVars=r.DefaultFeature.AutoExposure=False
+CVars=r.DefaultFeature.Bloom=False
+CVars=r.DefaultFeature.LensFlare=False
+CVars=r.DefaultFeature.MotionBlur=False
+CVars=r.DepthOfFieldQuality=0
+CVars=r.DetailMode=0
+CVars=r.EarlyZPass=0
+CVars=r.ExposureOffset=0.3
+CVars=r.HZBOcclusion=0
+CVars=r.LensFlareQuality=0
+CVars=r.LightFunctionQuality=0
+CVars=r.LightShaftQuality=0
+CVars=r.LightShafts=0
+CVars=r.MaxAnisotropy=0
+CVars=r.MotionBlurQuality=0
+CVars=r.PostProcessAAQuality=0
+CVars=r.ReflectionEnvironment=0
+CVars=r.RefractionQuality=0
+CVars=r.SSAOSmartBlur=0
+CVars=r.SSR.Quality=0
+CVars=r.SSS.SampleSet=0
+CVars=r.SSS.Scale=0
+CVars=r.SceneColorFringe.Max=0
+CVars=r.SceneColorFringeQuality=0
+CVars=r.Shadow.CSM.MaxCascades=1
+CVars=r.Shadow.CSM.TransitionScale=0
+CVars=r.Shadow.DistanceScale=0.1
+CVars=r.Shadow.MaxResolution=2
+CVars=r.Shadow.MinResolution=2
+CVars=r.Shadow.RadiusThreshold=0.1
+CVars=r.ShadowQuality=0
+CVars=r.TonemapperQuality=0
+CVars=r.TriangleOrderOptimization=1
+CVars=r.TrueSkyQuality=0
+CVars=r.UpsampleQuality=0
+CVars=r.ViewDistanceScale=0
+CVars=r.oneframethreadlag=1
+CVars=ShowFlag.LightFunctions=1
+CVars=t.maxfps=165


[WindowsNoEditor DeviceProfile]
DeviceType=WindowsNoEditor
BaseProfileName=Windows

[WindowsServer DeviceProfile]
DeviceType=WindowsServer
BaseProfileName=Windows

[IOS DeviceProfile]
DeviceType=IOS
BaseProfileName=
+CVars=r.BloomQuality=0
+CVars=r.DepthOfFieldQuality=0
+CVars=r.LightShaftQuality=0
+CVars=r.RefractionQuality=0

[iPad2 DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.RenderTargetSwitchWorkaround=1

[iPad3 DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.RenderTargetSwitchWorkaround=1

[iPad4 DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.RenderTargetSwitchWorkaround=1

[iPadAir DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.BloomQuality=1

[iPadMini DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.RenderTargetSwitchWorkaround=1

[iPadMini2 DeviceProfile]
DeviceType=IOS
BaseProfileName=iPadAir

[iPhone4 DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.RenderTargetSwitchWorkaround=1

[iPhone4S DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.RenderTargetSwitchWorkaround=1

[iPhone5 DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.RenderTargetSwitchWorkaround=1

[iPhone5S DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.MobileContentScaleFactor=2
+CVars=r.BloomQuality=1
+CVars=r.DepthOfFieldQuality=1
+CVars=r.LightShaftQuality=1

[iPodTouch5 DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.RenderTargetSwitchWorkaround=1

[iPhone6 DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.MobileContentScaleFactor=0
+CVars=r.BloomQuality=1
+CVars=r.DepthOfFieldQuality=1
+CVars=r.LightShaftQuality=1

[iPhone6Plus DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.MobileContentScaleFactor=0
+CVars=r.BloomQuality=1
+CVars=r.DepthOfFieldQuality=1
+CVars=r.LightShaftQuality=1

[Android DeviceProfile]
DeviceType=Android
BaseProfileName=
+CVars=r.MobileContentScaleFactor=1
+CVars=r.BloomQuality=0
+CVars=r.DepthOfFieldQuality=0
+CVars=r.LightShaftQuality=0
+CVars=r.RefractionQuality=0

[Android_Low DeviceProfile]
DeviceType=Android
BaseProfileName=Android
+CVars=r.MobileContentScaleFactor=0.5

[Android_Mid DeviceProfile]
DeviceType=Android
BaseProfileName=Android
+CVars=r.BloomQuality=1
+CVars=r.MobileContentScaleFactor=0.8

[Android_High DeviceProfile]
DeviceType=Android
BaseProfileName=Android
+CVars=r.BloomQuality=1
+CVars=r.DepthOfFieldQuality=1
+CVars=r.LightShaftQuality=1
+CVars=r.MobileContentScaleFactor=1.0

[Android_Unrecognized DeviceProfile]
DeviceType=Android
BaseProfileName=Android_Mid

[Android_Adreno320 DeviceProfile]
DeviceType=Android
BaseProfileName=Android_Mid

;This offset needs to be set for the mosaic fallback to work on Galaxy S4 (SAMSUNG-IGH-I337)
;+CVars=r.DemosaicVposOffset=0.5

[Android_Adreno330 DeviceProfile]
DeviceType=Android
BaseProfileName=Android_High

[Android_Adreno330_Ver53 DeviceProfile]
DeviceType=Android
BaseProfileName=Android_Adreno330
+CVars=r.DisjointTimerQueries=1

[PS4 DeviceProfile]
DeviceType=PS4
BaseProfileName=

[XboxOne DeviceProfile]
DeviceType=XboxOne
BaseProfileName=
; we output 10:10:10, not 8:8:8 so we don't need color quantization
+CVars=r.TonemapperQuality=0
; For SSAO we rely on TemporalAA (with a randomized sample pattern over time) so we can use less samples
+CVars=r.AmbientOcclusionSampleSetQuality=0
; less passes, and no upsampling as even upsampling costs some performance
+CVars=r.AmbientOcclusionLevels=1
; larger radius to compensate for fewer passes
+CVars=r.AmbientOcclusionRadiusScale=2


[HTML5 DeviceProfile]
DeviceType=HTML5
BaseProfileName=
+CVars=r.RefractionQuality=0

[Mac DeviceProfile]
DeviceType=Mac
BaseProfileName=

[MacNoEditor DeviceProfile]
DeviceType=MacNoEditor
BaseProfileName=Mac

[MacServer DeviceProfile]
DeviceType=MacServer
BaseProfileName=Mac

[WinRT DeviceProfile]
DeviceType=WinRT
BaseProfileName=

[Linux DeviceProfile]
DeviceType=Linux
BaseProfileName=
MeshLODSettings=
TextureLODSettings=

[LinuxNoEditor DeviceProfile]
DeviceType=LinuxNoEditor
BaseProfileName=Linux
MeshLODSettings=
TextureLODSettings=

[LinuxServer DeviceProfile]
DeviceType=LinuxServer
BaseProfileName=Linux
MeshLODSettings=
TextureLODSettings=
""",
        "HARD": """[DeviceProfiles]
+DeviceProfileNameAndTypes=Windows,Windows
+DeviceProfileNameAndTypes=WindowsNoEditor,WindowsNoEditor
+DeviceProfileNameAndTypes=WindowsServer,WindowsServer
+DeviceProfileNameAndTypes=IOS,IOS
+DeviceProfileNameAndTypes=iPad2,IOS
+DeviceProfileNameAndTypes=iPad3,IOS
+DeviceProfileNameAndTypes=iPad4,IOS
+DeviceProfileNameAndTypes=iPadAir,IOS
+DeviceProfileNameAndTypes=iPadMini,IOS
+DeviceProfileNameAndTypes=iPadMini2,IOS
+DeviceProfileNameAndTypes=iPhone4,IOS
+DeviceProfileNameAndTypes=iPhone4S,IOS
+DeviceProfileNameAndTypes=iPhone5,IOS
+DeviceProfileNameAndTypes=iPhone5S,IOS
+DeviceProfileNameAndTypes=iPodTouch5,IOS
+DeviceProfileNameAndTypes=iPhone6,IOS
+DeviceProfileNameAndTypes=iPhone6Plus,IOS
+DeviceProfileNameAndTypes=Android,Android
+DeviceProfileNameAndTypes=PS4,PS4
+DeviceProfileNameAndTypes=XboxOne,XboxOne
+DeviceProfileNameAndTypes=HTML5,HTML5
+DeviceProfileNameAndTypes=Mac,Mac
+DeviceProfileNameAndTypes=MacNoEditor,MacNoEditor
+DeviceProfileNameAndTypes=MacServer,MacServer
+DeviceProfileNameAndTypes=WinRT,WinRT
+DeviceProfileNameAndTypes=Linux,Linux
+DeviceProfileNameAndTypes=LinuxNoEditor,LinuxNoEditor
+DeviceProfileNameAndTypes=LinuxServer,LinuxServer

[Windows DeviceProfile]
DeviceType=Windows
BaseProfileName=
+CVars=FogDensity=0.0
+CVars=ShowFlag.AtmosphericFog=0
+CVars=ShowFlag.g=0
+CVars=ShowFlag.Game=0 
+CVars=ShowFlag.Tessellation=0
+CVars=ShowFlag.DepthOfField=0
+CVars=ShowFlag.Pivot=0
+CVars=ShowFlag.LevelColoration=0
+CVars=ShowFlag.LightComplexity=0
+CVars=ShowFlag.LightFunctions=1
+CVars=ShowFlag.Bounds=0
+CVars=ShowFlag.LightMapDensity=0
+CVars=ShowFlag.Materials=0
+CVars=foliage.UseOcclusionType=0
+CVars=ShowFlag.Brushes=0
+CVars=ShowFlag.GameplayDebug=1
+CVars=r.SceneColorFringe.Max=0
+CVars=r.SceneColorFringeQuality=0
+CVars=ShowFlag.VisualizeLPV=0
+CVars=t.maxfps=165
+CVars=SmoothedFrameRateRange=(LowerBound=(Type="ERangeBoundTypes::Inclusive",Value=60),UpperBound=(Type="ERangeBoundTypes::Exclusive",Value=70))
+CVars=TEXTUREGROUP_Character=(MinLODSize=1,MaxLODSize=4,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_CharacterNormalMap=(MinLODSize=1,MaxLODSize=4,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_CharacterSpecular=(MinLODSize=1,MaxLODSize=4,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_Cinematic=(MinLODSize=1,MaxLODSize=128,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_Effects=(MinLODSize=1,MaxLODSize=128,LODBias=0,MinMagFilter=linear,MipFilter=point)
+CVars=TEXTUREGROUP_EffectsNotFiltered=(MinLODSize=1,MaxLODSize=128,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_Lightmap=(MinLODSize=1,MaxLODSize=8,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_MobileFlattened=(MinLODSize=1,MaxLODSize=2,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_RenderTarget=(MinLODSize=1,MaxLODSize=128,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_Shadowmap=(MinLODSize=1,MaxLODSize=2,LODBias=0,MinMagFilter=aniso,MipFilter=point,NumStreamedMips=3)
+CVars=TEXTUREGROUP_Skybox=(MinLODSize=1,MaxLODSize=256,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_Terrain_Heightmap=(MinLODSize=1,MaxLODSize=2,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_Terrain_Weightmap=(MinLODSize=1,MaxLODSize=2,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_UI=(MinLODSize=1,MaxLODSize=256,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_Vehicle=(MinLODSize=1,MaxLODSize=256,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_VehicleNormalMap=(MinLODSize=1,MaxLODSize=256,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_VehicleSpecular=(MinLODSize=1,MaxLODSize=256,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_Weapon=(MinLODSize=1,MaxLODSize=64,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_WeaponNormalMap=(MinLODSize=1,MaxLODSize=64,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_WeaponSpecular=(MinLODSize=1,MaxLODSize=64,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_World=(MinLODSize=1,MaxLODSize=2,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_WorldNormalMap=(MinLODSize=1,MaxLODSize=2,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_WorldSpecular=(MinLODSize=1,MaxLODSize=2,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=bDisablePhysXHardwareSupport=True
+CVars=bFirstRun=False
+CVars=bSmoothFrameRate=true
+CVars=r.AOTrimOldRecordsFraction=0
+CVars=r.AmbientOcclusionLevels=0
+CVars=r.Atmosphere=0
+CVars=r.BloomQuality=0
+CVars=r.ClearWithExcludeRects=0
+CVars=r.CompileShadersForDevelopment=0
+CVars=r.CustomDepth=0
+CVars=r.DefaultFeature.AmbientOcclusion=False
+CVars=r.DefaultFeature.AntiAliasing=0
+CVars=r.DefaultFeature.AutoExposure=False
+CVars=r.DefaultFeature.Bloom=False
+CVars=r.DefaultFeature.LensFlare=False
+CVars=r.DefaultFeature.MotionBlur=False
+CVars=r.DepthOfFieldQuality=0
+CVars=r.DetailMode=0
+CVars=r.EarlyZPass=0
+CVars=r.ExposureOffset=0.3
+CVars=r.HZBOcclusion=0
+CVars=r.LensFlareQuality=0
+CVars=r.LightFunctionQuality=0
+CVars=r.LightShaftQuality=0
+CVars=r.LightShafts=0
+CVars=r.MaxAnisotropy=0
+CVars=r.MotionBlurQuality=0
+CVars=r.PostProcessAAQuality=0
+CVars=r.ReflectionEnvironment=0
+CVars=r.RefractionQuality=0
+CVars=r.SSAOSmartBlur=0
+CVars=r.SSR.Quality=0
+CVars=r.SSS.Scale=0
+CVars=r.SceneColorFringe.Max=0
+CVars=r.SceneColorFringeQuality=0
+CVars=r.Shadow.CSM.MaxCascades=1
+CVars=r.Shadow.CSM.TransitionScale=0
+CVars=r.Shadow.DistanceScale=0.1
+CVars=r.Shadow.MaxResolution=2
+CVars=r.Shadow.MinResolution=2
+CVars=r.Shadow.RadiusThreshold=0.1
+CVars=r.ShadowQuality=0
+CVars=r.TonemapperQuality=0
+CVars=r.TriangleOrderOptimization=1
+CVars=r.TrueSkyQuality=0
+CVars=r.UpsampleQuality=0
+CVars=r.ViewDistanceScale=3
+CVars=r.oneframethreadlag=1
+CVars=ShowFlag.ReflectionEnvironment=0
+CVars=ShowFlag.ReflectionOverride=0
+CVars=ShowFlag.Refraction=0
+CVars=ShowFlag.SelectionOutline=0
+CVars=ShowFlag.ShaderComplexity=0
+CVars=ShowFlag.ShadowFrustums=0
+CVars=ShowFlag.ShadowsFromEditorHiddenActors=0
+CVars=ShowFlag.SkeletalMeshes=0
+CVars=ShowFlag.SkyLighting=0
+CVars=ShowFlag.Snap=0
+CVars=ShowFlag.Specular=0
+CVars=ShowFlag.SpotLights=0
+CVars=ShowFlag.StaticMeshes=0
+CVars=ShowFlag.StationaryLightOverlap=0
+CVars=ShowFlag.StereoRendering=0
+CVars=ShowFlag.SubsurfaceScattering=0
+CVars=ShowFlag.TemporalAA=0
+CVars=ShowFlag.VisualizeDOF=0
+CVars=ShowFlag.VisualizeDistanceFieldAO=0
+CVars=ShowFlag.VisualizeHDR=0
+CVars=ShowFlag.VisualizeLPV=0
+CVars=ShowFlag.VisualizeLightCulling=0
+CVars=ShowFlag.VisualizeMotionBlur=0
+CVars=ShowFlag.VisualizeOutOfBoundsPixels=0
+CVars=ShowFlag.VisualizeSSR=0
+CVars=ShowFlag.VisualizeSenses=0
+CVars=ShowFlag.Wireframe=0
+CVars=ShowFlag.LightComplexity=0
+CVars=ShowFlag.SeparateTranslucency=0
+CVars=ShowFlag.GameplayDebug=0
+CVars=foliage.UseOcclusionType=0
+CVars=ShowFloatingDamageText=True
+CVars=FogDensity=0.0
+CVars=FrameRateCap=144
+CVars=FrameRateMinimum=144
+CVars=MaxES2PixelShaderAdditiveComplexityCount=45
+CVars=MaxPixelShaderAdditiveComplexityCount=128
+CVars=MaxSmoothedFrameRate=144
+CVars=MinDesiredFrameRate=120
+CVars=MinSmoothedFrameRate=5
+CVars=NearClipPlane=12.0
+CVars=ShowFlag.AmbientOcclusion=0
+CVars=ShowFlag.AntiAliasing=0
+CVars=ShowFlag.Atmosphere=0
+CVars=ShowFlag.AtmosphericFog=0
+CVars=ShowFlag.AudioRadius=0
+CVars=ShowFlag.BSP=0
+CVars=ShowFlag.BSPSplit=0
+CVars=ShowFlag.BSPTriangles=0
+CVars=ShowFlag.BillboardSprites=0
+CVars=ShowFlag.Brushes=0
+CVars=ShowFlag.BuilderBrush=0
+CVars=ShowFlag.CameraAspectRatioBars=0
+CVars=ShowFlag.CameraFrustums=0
+CVars=ShowFlag.CameraImperfections=0
+CVars=ShowFlag.CameraInterpolation=0
+CVars=ShowFlag.CameraSafeFrames=0
+CVars=ShowFlag.ColorGrading=0
+CVars=ShowFlag.CompositeEditorPrimitives=0
+CVars=ShowFlag.Constraints=0
+CVars=ShowFlag.Cover=0
+CVars=ShowFlag.Decals=0
+CVars=ShowFlag.DeferredLighting=0
+CVars=ShowFlag.DepthOfField=0
+CVars=ShowFlag.Diffuse=0
+CVars=ShowFlag.DirectLighting=0
+CVars=ShowFlag.DirectionalLights=0
+CVars=ShowFlag.DistanceCulledPrimitives=0
+CVars=ShowFlag.DistanceFieldAO=0
+CVars=ShowFlag.DynamicShadows=0
+CVars=ShowFlag.Editor=0
+CVars=ShowFlag.EyeAdaptation=0
+CVars=ShowFlag.Fog=0
+CVars=ShowFlag.Game=0
+CVars=ShowFlag.LOD=0
+CVars=ShowFlag.Landscape=0
+CVars=ShowFlag.LargeVertices=0
+CVars=ShowFlag.LensFlares=0
+CVars=ShowFlag.LevelColoration=0
+CVars=ShowFlag.LightComplexity=0
+CVars=ShowFlag.LightInfluences=0
+CVars=ShowFlag.LightMapDensity=0
+CVars=ShowFlag.LightRadius=0
+CVars=ShowFlag.LightShafts=0
+CVars=ShowFlag.Lighting=0
+CVars=ShowFlag.LpvLightingOnly=0
+CVars=ShowFlag.Materials=0
+CVars=ShowFlag.MeshEdges=0
+CVars=ShowFlag.MotionBlur=0
+CVars=ShowFlag.OnScreenDebug=0
+CVars=ShowFlag.OverrideDiffuseAndSpecular=0
+CVars=ShowFlag.Paper2DSprites=0
+CVars=ShowFlag.Particles=0
+CVars=ShowFlag.Pivot=0
+CVars=ShowFlag.PointLights=0
+CVars=ShowFlag.PostProcessMaterial=0
+CVars=ShowFlag.PostProcessing=0
+CVars=ShowFlag.PrecomputedVisibility=0
+CVars=ShowFlag.PreviewShadowsIndicator=0
+CVars=ShowFlag.ReflectionEnvironment=0
+CVars=ShowFlag.ReflectionOverride=0
+CVars=ShowFlag.Refraction=0
+CVars=ShowFlag.SelectionOutline=0
+CVars=ShowFlag.ShaderComplexity=0
+CVars=ShowFlag.ShadowFrustums=0
+CVars=ShowFlag.ShadowsFromEditorHiddenActors=0
+CVars=ShowFlag.SkeletalMeshes=0
+CVars=ShowFlag.SkyLighting=0
+CVars=ShowFlag.Snap=0
+CVars=ShowFlag.Specular=0
+CVars=ShowFlag.SpotLights=0
+CVars=ShowFlag.StaticMeshes=0
+CVars=ShowFlag.StationaryLightOverlap=0
+CVars=ShowFlag.StereoRendering=0
+CVars=ShowFlag.SubsurfaceScattering=0
+CVars=ShowFlag.TemporalAA=0
+CVars=ShowFlag.Tessellation=0
+CVars=ShowFlag.TestImage=0
+CVars=ShowFlag.TextRender=0
+CVars=ShowFlag.TexturedLightProfiles=0
+CVars=ShowFlag.Tonemapper=0
+CVars=ShowFlag.Translucency=0
+CVars=ShowFlag.VectorFields=0
+CVars=ShowFlag.VertexColors=0
+CVars=ShowFlag.Vignette=0
+CVars=ShowFlag.VisualizeAdaptiveDOF=0
+CVars=ShowFlag.VisualizeBuffer=0
+CVars=ShowFlag.VisualizeDOF=0
+CVars=ShowFlag.VisualizeDistanceFieldAO=0
+CVars=ShowFlag.VisualizeHDR=0
+CVars=ShowFlag.VisualizeLPV=0
+CVars=ShowFlag.VisualizeLightCulling=0
+CVars=ShowFlag.VisualizeMotionBlur=0
+CVars=ShowFlag.VisualizeOutOfBoundsPixels=0
+CVars=ShowFlag.VisualizeSSR=0
+CVars=ShowFlag.VisualizeSenses=0


[WindowsNoEditor DeviceProfile]
DeviceType=WindowsNoEditor
BaseProfileName=Windows

[WindowsServer DeviceProfile]
DeviceType=WindowsServer
BaseProfileName=Windows

[IOS DeviceProfile]
DeviceType=IOS
BaseProfileName=
+CVars=r.BloomQuality=0
+CVars=r.DepthOfFieldQuality=0
+CVars=r.LightShaftQuality=0
+CVars=r.RefractionQuality=0

[iPad2 DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.RenderTargetSwitchWorkaround=1

[iPad3 DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.RenderTargetSwitchWorkaround=1

[iPad4 DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.RenderTargetSwitchWorkaround=1

[iPadAir DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.BloomQuality=1

[iPadMini DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.RenderTargetSwitchWorkaround=1

[iPadMini2 DeviceProfile]
DeviceType=IOS
BaseProfileName=iPadAir

[iPhone4 DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.RenderTargetSwitchWorkaround=1

[iPhone4S DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.RenderTargetSwitchWorkaround=1

[iPhone5 DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.RenderTargetSwitchWorkaround=1

[iPhone5S DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.MobileContentScaleFactor=2
+CVars=r.BloomQuality=1
+CVars=r.DepthOfFieldQuality=1
+CVars=r.LightShaftQuality=1

[iPodTouch5 DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.RenderTargetSwitchWorkaround=1

[iPhone6 DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.MobileContentScaleFactor=0
+CVars=r.BloomQuality=1
+CVars=r.DepthOfFieldQuality=1
+CVars=r.LightShaftQuality=1

[iPhone6Plus DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.MobileContentScaleFactor=0
+CVars=r.BloomQuality=1
+CVars=r.DepthOfFieldQuality=1
+CVars=r.LightShaftQuality=1

[Android DeviceProfile]
DeviceType=Android
BaseProfileName=
+CVars=r.MobileContentScaleFactor=1
+CVars=r.BloomQuality=0
+CVars=r.DepthOfFieldQuality=0
+CVars=r.LightShaftQuality=0
+CVars=r.RefractionQuality=0

[Android_Low DeviceProfile]
DeviceType=Android
BaseProfileName=Android
+CVars=r.MobileContentScaleFactor=0.5

[Android_Mid DeviceProfile]
DeviceType=Android
BaseProfileName=Android
+CVars=r.BloomQuality=1
+CVars=r.MobileContentScaleFactor=0.8

[Android_High DeviceProfile]
DeviceType=Android
BaseProfileName=Android
+CVars=r.BloomQuality=1
+CVars=r.DepthOfFieldQuality=1
+CVars=r.LightShaftQuality=1
+CVars=r.MobileContentScaleFactor=1.0

[Android_Unrecognized DeviceProfile]
DeviceType=Android
BaseProfileName=Android_Mid

[Android_Adreno320 DeviceProfile]
DeviceType=Android
BaseProfileName=Android_Mid

;This offset needs to be set for the mosaic fallback to work on Galaxy S4 (SAMSUNG-IGH-I337)
;+CVars=r.DemosaicVposOffset=0.5

[Android_Adreno330 DeviceProfile]
DeviceType=Android
BaseProfileName=Android_High

[Android_Adreno330_Ver53 DeviceProfile]
DeviceType=Android
BaseProfileName=Android_Adreno330
+CVars=r.DisjointTimerQueries=1

[PS4 DeviceProfile]
DeviceType=PS4
BaseProfileName=

[XboxOne DeviceProfile]
DeviceType=XboxOne
BaseProfileName=
; we output 10:10:10, not 8:8:8 so we don't need color quantization
+CVars=r.TonemapperQuality=0
; For SSAO we rely on TemporalAA (with a randomized sample pattern over time) so we can use less samples
+CVars=r.AmbientOcclusionSampleSetQuality=0
; less passes, and no upsampling as even upsampling costs some performance
+CVars=r.AmbientOcclusionLevels=1
; larger radius to compensate for fewer passes
+CVars=r.AmbientOcclusionRadiusScale=2


[HTML5 DeviceProfile]
DeviceType=HTML5
BaseProfileName=
+CVars=r.RefractionQuality=0

[Mac DeviceProfile]
DeviceType=Mac
BaseProfileName=

[MacNoEditor DeviceProfile]
DeviceType=MacNoEditor
BaseProfileName=Mac

[MacServer DeviceProfile]
DeviceType=MacServer
BaseProfileName=Mac

[WinRT DeviceProfile]
DeviceType=WinRT
BaseProfileName=

[Linux DeviceProfile]
DeviceType=Linux
BaseProfileName=
MeshLODSettings=
TextureLODSettings=

[LinuxNoEditor DeviceProfile]
DeviceType=LinuxNoEditor
BaseProfileName=Linux
MeshLODSettings=
TextureLODSettings=

[LinuxServer DeviceProfile]
DeviceType=LinuxServer
BaseProfileName=Linux
MeshLODSettings=
TextureLODSettings=
""",
        "PVP_SPYGLASS": """[DeviceProfiles]
+DeviceProfileNameAndTypes=Windows,Windows
+DeviceProfileNameAndTypes=WindowsNoEditor,WindowsNoEditor
+DeviceProfileNameAndTypes=WindowsServer,WindowsServer
+DeviceProfileNameAndTypes=IOS,IOS
+DeviceProfileNameAndTypes=iPad2,IOS
+DeviceProfileNameAndTypes=iPad3,IOS
+DeviceProfileNameAndTypes=iPad4,IOS
+DeviceProfileNameAndTypes=iPadAir,IOS
+DeviceProfileNameAndTypes=iPadMini,IOS
+DeviceProfileNameAndTypes=iPadMini2,IOS
+DeviceProfileNameAndTypes=iPhone4,IOS
+DeviceProfileNameAndTypes=iPhone4S,IOS
+DeviceProfileNameAndTypes=iPhone5,IOS
+DeviceProfileNameAndTypes=iPhone5S,IOS
+DeviceProfileNameAndTypes=iPodTouch5,IOS
+DeviceProfileNameAndTypes=iPhone6,IOS
+DeviceProfileNameAndTypes=iPhone6Plus,IOS
+DeviceProfileNameAndTypes=Android,Android
+DeviceProfileNameAndTypes=PS4,PS4
+DeviceProfileNameAndTypes=XboxOne,XboxOne
+DeviceProfileNameAndTypes=HTML5,HTML5
+DeviceProfileNameAndTypes=Mac,Mac
+DeviceProfileNameAndTypes=MacNoEditor,MacNoEditor
+DeviceProfileNameAndTypes=MacServer,MacServer
+DeviceProfileNameAndTypes=WinRT,WinRT
+DeviceProfileNameAndTypes=Linux,Linux
+DeviceProfileNameAndTypes=LinuxNoEditor,LinuxNoEditor
+DeviceProfileNameAndTypes=LinuxServer,LinuxServer

[Windows DeviceProfile]
DeviceType=Windows
BaseProfileName=
+CVars=foliage.UseOcclusionType=0
+CVars=ShowFloatingDamageText=True
+CVars=FogDensity=0.0
+CVars=FrameRateCap=144
+CVars=FrameRateMinimum=144
+CVars=MaxES2PixelShaderAdditiveComplexityCount=45
+CVars=MaxPixelShaderAdditiveComplexityCount=128
+CVars=MaxSmoothedFrameRate=144
+CVars=MinDesiredFrameRate=70
+CVars=MinSmoothedFrameRate=5
+CVars=NearClipPlane=12.0
+CVars=ShowFlag.AmbientOcclusion=0
+CVars=ShowFlag.AntiAliasing=0
+CVars=ShowFlag.Atmosphere=0
+CVars=ShowFlag.AtmosphericFog=0
+CVars=ShowFlag.AudioRadius=0
+CVars=ShowFlag.BSP=0
+CVars=ShowFlag.BSPSplit=0
+CVars=ShowFlag.BSPTriangles=0
+CVars=ShowFlag.BillboardSprites=0
+CVars=ShowFlag.Brushes=0
+CVars=ShowFlag.BuilderBrush=0
+CVars=ShowFlag.CameraAspectRatioBars=0
+CVars=ShowFlag.CameraFrustums=0
+CVars=ShowFlag.CameraImperfections=0
+CVars=ShowFlag.CameraInterpolation=0
+CVars=ShowFlag.CameraSafeFrames=0
+CVars=ShowFlag.ColorGrading=0
+CVars=ShowFlag.CompositeEditorPrimitives=0
+CVars=ShowFlag.Constraints=0
+CVars=ShowFlag.Cover=0
+CVars=ShowFlag.Decals=0
+CVars=ShowFlag.DeferredLighting=0
+CVars=ShowFlag.DepthOfField=0
+CVars=ShowFlag.Diffuse=0
+CVars=ShowFlag.DirectLighting=0
+CVars=ShowFlag.DirectionalLights=0
+CVars=ShowFlag.DistanceCulledPrimitives=0
+CVars=ShowFlag.DistanceFieldAO=0
+CVars=ShowFlag.DynamicShadows=0
+CVars=ShowFlag.Editor=0
+CVars=ShowFlag.EyeAdaptation=0
+CVars=ShowFlag.Fog=1
+CVars=ShowFlag.Game=0
+CVars=ShowFlag.LOD=0
+CVars=ShowFlag.Landscape=0
+CVars=ShowFlag.LargeVertices=0
+CVars=ShowFlag.LensFlares=0
+CVars=ShowFlag.LevelColoration=0
+CVars=ShowFlag.LightComplexity=0 ;static
+CVars=ShowFlag.LightInfluences=0
+CVars=ShowFlag.LightMapDensity=0
+CVars=ShowFlag.LightRadius=0
+CVars=ShowFlag.LightShafts=0 ;static
+CVars=ShowFlag.Lighting=0
+CVars=ShowFlag.LpvLightingOnly=0
;+CVars=ShowFlag.Materials=0 ;outlines
+CVars=ShowFlag.MeshEdges=0
+CVars=ShowFlag.MotionBlur=0
+CVars=ShowFlag.OnScreenDebug=0
+CVars=ShowFlag.OverrideDiffuseAndSpecular=0
+CVars=ShowFlag.Paper2DSprites=0
+CVars=ShowFlag.Particles=0
+CVars=ShowFlag.Pivot=0
+CVars=ShowFlag.PointLights=0
+CVars=ShowFlag.PostProcessMaterial=0
+CVars=ShowFlag.PostProcessing=0
+CVars=ShowFlag.PrecomputedVisibility=0
+CVars=ShowFlag.PreviewShadowsIndicator=0
+CVars=ShowFlag.ReflectionEnvironment=0
+CVars=ShowFlag.ReflectionOverride=0
+CVars=ShowFlag.Refraction=0
+CVars=ShowFlag.SelectionOutline=0
+CVars=ShowFlag.ShaderComplexity=0 ;static
+CVars=ShowFlag.ShadowFrustums=0
+CVars=ShowFlag.ShadowsFromEditorHiddenActors=0
+CVars=ShowFlag.SkeletalMeshes=0
+CVars=ShowFlag.SkyLighting=0
+CVars=ShowFlag.Snap=0
+CVars=ShowFlag.Specular=0
+CVars=ShowFlag.SpotLights=0
+CVars=ShowFlag.StaticMeshes=0
+CVars=ShowFlag.StationaryLightOverlap=0
+CVars=ShowFlag.StereoRendering=0
+CVars=ShowFlag.SubsurfaceScattering=0
+CVars=ShowFlag.TemporalAA=0
+CVars=ShowFlag.Tessellation=0
+CVars=ShowFlag.TestImage=0
+CVars=ShowFlag.TextRender=0
+CVars=ShowFlag.TexturedLightProfiles=0
+CVars=ShowFlag.Tonemapper=0
+CVars=ShowFlag.Translucency=0
+CVars=ShowFlag.VectorFields=0+CVars=FogDensity=0.0
+CVars=ShowFlag.AtmosphericFog=0
+CVars=ShowFlag.g=0
+CVars=ShowFlag.Game=0 
+CVars=ShowFlag.Tessellation=0
+CVars=ShowFlag.DepthOfField=0
+CVars=ShowFlag.Pivot=0
+CVars=ShowFlag.LevelColoration=0
+CVars=ShowFlag.LightComplexity=0
+CVars=ShowFlag.LightFunctions=1
+CVars=ShowFlag.Bounds=0
+CVars=ShowFlag.LightMapDensity=0
+CVars=ShowFlag.Materials=0
+CVars=foliage.UseOcclusionType=0
+CVars=ShowFlag.Brushes=0
+CVars=ShowFlag.GameplayDebug=1
+CVars=r.SceneColorFringe.Max=0
+CVars=r.SceneColorFringeQuality=0
+CVars=ShowFlag.VisualizeLPV=0
+CVars=t.maxfps=165
+CVars=SmoothedFrameRateRange=(LowerBound=(Type="ERangeBoundTypes::Inclusive",Value=60),UpperBound=(Type="ERangeBoundTypes::Exclusive",Value=70))
+CVars=TEXTUREGROUP_Character=(MinLODSize=1,MaxLODSize=4,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_CharacterNormalMap=(MinLODSize=1,MaxLODSize=4,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_CharacterSpecular=(MinLODSize=1,MaxLODSize=4,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_Cinematic=(MinLODSize=1,MaxLODSize=128,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_Effects=(MinLODSize=1,MaxLODSize=128,LODBias=0,MinMagFilter=linear,MipFilter=point)
+CVars=TEXTUREGROUP_EffectsNotFiltered=(MinLODSize=1,MaxLODSize=128,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_Lightmap=(MinLODSize=1,MaxLODSize=8,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_MobileFlattened=(MinLODSize=1,MaxLODSize=2,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_RenderTarget=(MinLODSize=1,MaxLODSize=128,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_Shadowmap=(MinLODSize=1,MaxLODSize=2,LODBias=0,MinMagFilter=aniso,MipFilter=point,NumStreamedMips=3)
+CVars=TEXTUREGROUP_Skybox=(MinLODSize=1,MaxLODSize=256,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_Terrain_Heightmap=(MinLODSize=1,MaxLODSize=2,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_Terrain_Weightmap=(MinLODSize=1,MaxLODSize=2,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_UI=(MinLODSize=1,MaxLODSize=256,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_Vehicle=(MinLODSize=1,MaxLODSize=256,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_VehicleNormalMap=(MinLODSize=1,MaxLODSize=256,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_VehicleSpecular=(MinLODSize=1,MaxLODSize=256,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_Weapon=(MinLODSize=1,MaxLODSize=64,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_WeaponNormalMap=(MinLODSize=1,MaxLODSize=64,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_WeaponSpecular=(MinLODSize=1,MaxLODSize=64,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_World=(MinLODSize=1,MaxLODSize=2,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_WorldNormalMap=(MinLODSize=1,MaxLODSize=2,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_WorldSpecular=(MinLODSize=1,MaxLODSize=2,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=bDisablePhysXHardwareSupport=True
+CVars=bFirstRun=False
+CVars=bSmoothFrameRate=true
+CVars=r.AOTrimOldRecordsFraction=0
+CVars=r.AmbientOcclusionLevels=0
+CVars=r.Atmosphere=0
+CVars=r.BloomQuality=0
+CVars=r.ClearWithExcludeRects=0
+CVars=r.CompileShadersForDevelopment=0
+CVars=r.CustomDepth=0
+CVars=r.DefaultFeature.AmbientOcclusion=False
+CVars=r.DefaultFeature.AntiAliasing=0
+CVars=r.DefaultFeature.AutoExposure=False
+CVars=r.DefaultFeature.Bloom=False
+CVars=r.DefaultFeature.LensFlare=False
+CVars=r.DefaultFeature.MotionBlur=False
+CVars=r.DepthOfFieldQuality=0
+CVars=r.DetailMode=0
+CVars=r.EarlyZPass=0
+CVars=r.ExposureOffset=0.3
+CVars=r.HZBOcclusion=0
+CVars=r.LensFlareQuality=0
+CVars=r.LightFunctionQuality=0
+CVars=r.LightShaftQuality=0
+CVars=r.LightShafts=0
+CVars=r.MaxAnisotropy=0
+CVars=r.MotionBlurQuality=0
+CVars=r.PostProcessAAQuality=0
+CVars=r.ReflectionEnvironment=0
+CVars=r.RefractionQuality=0
+CVars=r.SSAOSmartBlur=0
+CVars=r.SSR.Quality=0
+CVars=r.SSS.Scale=0
+CVars=r.SceneColorFringe.Max=0
+CVars=r.SceneColorFringeQuality=0
+CVars=r.Shadow.CSM.MaxCascades=1
+CVars=r.Shadow.CSM.TransitionScale=0
+CVars=r.Shadow.DistanceScale=0.1
+CVars=r.Shadow.MaxResolution=2
+CVars=r.Shadow.MinResolution=2
+CVars=r.Shadow.RadiusThreshold=0.1
+CVars=r.ShadowQuality=0
+CVars=r.TonemapperQuality=0
+CVars=r.TriangleOrderOptimization=1
+CVars=r.TrueSkyQuality=0
+CVars=r.UpsampleQuality=0
+CVars=r.ViewDistanceScale=3
+CVars=r.oneframethreadlag=1
+CVars=ShowFlag.ReflectionEnvironment=0
+CVars=ShowFlag.ReflectionOverride=0
+CVars=ShowFlag.Refraction=0
+CVars=ShowFlag.SelectionOutline=0
+CVars=ShowFlag.ShaderComplexity=0
+CVars=ShowFlag.ShadowFrustums=0
+CVars=ShowFlag.ShadowsFromEditorHiddenActors=0
+CVars=ShowFlag.SkeletalMeshes=0
+CVars=ShowFlag.SkyLighting=0
+CVars=ShowFlag.Snap=0
+CVars=ShowFlag.Specular=0
+CVars=ShowFlag.SpotLights=0
+CVars=ShowFlag.StaticMeshes=0
+CVars=ShowFlag.StationaryLightOverlap=0
+CVars=ShowFlag.StereoRendering=0
+CVars=ShowFlag.SubsurfaceScattering=0
+CVars=ShowFlag.TemporalAA=0
+CVars=ShowFlag.VisualizeDOF=0
+CVars=ShowFlag.VisualizeDistanceFieldAO=0
+CVars=ShowFlag.VisualizeHDR=0
+CVars=ShowFlag.VisualizeLPV=0
+CVars=ShowFlag.VisualizeLightCulling=0
+CVars=ShowFlag.VisualizeMotionBlur=0
+CVars=ShowFlag.VisualizeOutOfBoundsPixels=0
+CVars=ShowFlag.VisualizeSSR=0
+CVars=ShowFlag.VisualizeSenses=0
+CVars=ShowFlag.Wireframe=0
+CVars=ShowFlag.LightComplexity=0
+CVars=ShowFlag.SeparateTranslucency=0
+CVars=ShowFlag.GameplayDebug=0
+CVars=foliage.UseOcclusionType=0
+CVars=ShowFloatingDamageText=True
+CVars=FogDensity=0.0
+CVars=FrameRateCap=144
+CVars=FrameRateMinimum=144
+CVars=MaxES2PixelShaderAdditiveComplexityCount=45
+CVars=MaxPixelShaderAdditiveComplexityCount=128
+CVars=MaxSmoothedFrameRate=144
+CVars=MinDesiredFrameRate=120
+CVars=MinSmoothedFrameRate=5
+CVars=NearClipPlane=12.0
+CVars=ShowFlag.AmbientOcclusion=0
+CVars=ShowFlag.AntiAliasing=0
+CVars=ShowFlag.Atmosphere=0
+CVars=ShowFlag.AtmosphericFog=0
+CVars=ShowFlag.AudioRadius=0
+CVars=ShowFlag.BSP=0
+CVars=ShowFlag.BSPSplit=0
+CVars=ShowFlag.BSPTriangles=0
+CVars=ShowFlag.BillboardSprites=0
+CVars=ShowFlag.Brushes=0
+CVars=ShowFlag.BuilderBrush=0
+CVars=ShowFlag.CameraAspectRatioBars=0
+CVars=ShowFlag.CameraFrustums=0
+CVars=ShowFlag.CameraImperfections=0
+CVars=ShowFlag.CameraInterpolation=0
+CVars=ShowFlag.CameraSafeFrames=0
+CVars=ShowFlag.ColorGrading=0
+CVars=ShowFlag.CompositeEditorPrimitives=0
+CVars=ShowFlag.Constraints=0
+CVars=ShowFlag.Cover=0
+CVars=ShowFlag.Decals=0
+CVars=ShowFlag.DeferredLighting=0
+CVars=ShowFlag.DepthOfField=0
+CVars=ShowFlag.Diffuse=0
+CVars=ShowFlag.DirectLighting=0
+CVars=ShowFlag.DirectionalLights=0
+CVars=ShowFlag.DistanceCulledPrimitives=0
+CVars=ShowFlag.DistanceFieldAO=0
+CVars=ShowFlag.DynamicShadows=0
+CVars=ShowFlag.Editor=0
+CVars=ShowFlag.EyeAdaptation=0
+CVars=ShowFlag.Fog=0
+CVars=ShowFlag.Game=0
+CVars=ShowFlag.LOD=0
+CVars=ShowFlag.Landscape=0
+CVars=ShowFlag.LargeVertices=0
+CVars=ShowFlag.LensFlares=0
+CVars=ShowFlag.LevelColoration=0
+CVars=ShowFlag.LightComplexity=0
+CVars=ShowFlag.LightInfluences=0
+CVars=ShowFlag.LightMapDensity=0
+CVars=ShowFlag.LightRadius=0
+CVars=ShowFlag.LightShafts=0
+CVars=ShowFlag.Lighting=0
+CVars=ShowFlag.LpvLightingOnly=0
+CVars=ShowFlag.Materials=0
+CVars=ShowFlag.MeshEdges=0
+CVars=ShowFlag.MotionBlur=0
+CVars=ShowFlag.OnScreenDebug=0
+CVars=ShowFlag.OverrideDiffuseAndSpecular=0
+CVars=ShowFlag.Paper2DSprites=0
+CVars=ShowFlag.Particles=0
+CVars=ShowFlag.Pivot=0
+CVars=ShowFlag.PointLights=0
+CVars=ShowFlag.PostProcessMaterial=0
+CVars=ShowFlag.PostProcessing=0
+CVars=ShowFlag.PrecomputedVisibility=0
+CVars=ShowFlag.PreviewShadowsIndicator=0
+CVars=ShowFlag.ReflectionEnvironment=0
+CVars=ShowFlag.ReflectionOverride=0
+CVars=ShowFlag.Refraction=0
+CVars=ShowFlag.SelectionOutline=0
+CVars=ShowFlag.ShaderComplexity=0
+CVars=ShowFlag.ShadowFrustums=0
+CVars=ShowFlag.ShadowsFromEditorHiddenActors=0
+CVars=ShowFlag.SkeletalMeshes=0
+CVars=ShowFlag.SkyLighting=0
+CVars=ShowFlag.Snap=0
+CVars=ShowFlag.Specular=0
+CVars=ShowFlag.SpotLights=0
+CVars=ShowFlag.StaticMeshes=0
+CVars=ShowFlag.StationaryLightOverlap=0
+CVars=ShowFlag.StereoRendering=0
+CVars=ShowFlag.SubsurfaceScattering=0
+CVars=ShowFlag.TemporalAA=0
+CVars=ShowFlag.Tessellation=0
+CVars=ShowFlag.TestImage=0
+CVars=ShowFlag.TextRender=0
+CVars=ShowFlag.TexturedLightProfiles=0
+CVars=ShowFlag.Tonemapper=0
+CVars=ShowFlag.Translucency=0
+CVars=ShowFlag.VectorFields=0
+CVars=ShowFlag.VertexColors=0
+CVars=ShowFlag.Vignette=0
+CVars=ShowFlag.VisualizeAdaptiveDOF=0
+CVars=ShowFlag.VisualizeBuffer=0
+CVars=ShowFlag.VisualizeDOF=0
+CVars=ShowFlag.VisualizeDistanceFieldAO=0
+CVars=ShowFlag.VisualizeHDR=0
+CVars=ShowFlag.VisualizeLPV=0
+CVars=ShowFlag.VisualizeLightCulling=0
+CVars=ShowFlag.VisualizeMotionBlur=0
+CVars=ShowFlag.VisualizeOutOfBoundsPixels=0
+CVars=ShowFlag.VisualizeSSR=0
+CVars=ShowFlag.VisualizeSenses=0
+CVars=ShowFlag.VertexColors=0
+CVars=ShowFlag.Vignette=0
+CVars=ShowFlag.VisualizeAdaptiveDOF=0
+CVars=ShowFlag.VisualizeBuffer=0
+CVars=ShowFlag.VisualizeDOF=0
+CVars=ShowFlag.VisualizeDistanceFieldAO=0
+CVars=ShowFlag.VisualizeHDR=0
+CVars=ShowFlag.VisualizeLPV=0
+CVars=ShowFlag.VisualizeLightCulling=0
+CVars=ShowFlag.VisualizeMotionBlur=0
+CVars=ShowFlag.VisualizeOutOfBoundsPixels=0
+CVars=ShowFlag.VisualizeSSR=0
+CVars=ShowFlag.VisualizeSenses=0
+CVars=ShowFlag.VolumeLightingSamples=0
+CVars=ShowFlag.Wireframe=0
+CVars=SmoothedFrameRateRange=(LowerBound=(Type="ERangeBoundTypes::Inclusive",Value=60),UpperBound=(Type="ERangeBoundTypes::Exclusive",Value=70))
+CVars=TEXTUREGROUP_Character=(MinLODSize=1,MaxLODSize=4,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_CharacterNormalMap=(MinLODSize=1,MaxLODSize=4,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_CharacterSpecular=(MinLODSize=1,MaxLODSize=4,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_Cinematic=(MinLODSize=1,MaxLODSize=128,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_Effects=(MinLODSize=1,MaxLODSize=128,LODBias=0,MinMagFilter=linear,MipFilter=point)
+CVars=TEXTUREGROUP_EffectsNotFiltered=(MinLODSize=1,MaxLODSize=128,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_Lightmap=(MinLODSize=1,MaxLODSize=8,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_MobileFlattened=(MinLODSize=1,MaxLODSize=2,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_RenderTarget=(MinLODSize=1,MaxLODSize=128,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_Shadowmap=(MinLODSize=1,MaxLODSize=2,LODBias=0,MinMagFilter=aniso,MipFilter=point,NumStreamedMips=3)
+CVars=TEXTUREGROUP_Skybox=(MinLODSize=1,MaxLODSize=256,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_Terrain_Heightmap=(MinLODSize=1,MaxLODSize=2,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_Terrain_Weightmap=(MinLODSize=1,MaxLODSize=2,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_UI=(MinLODSize=1,MaxLODSize=256,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_Vehicle=(MinLODSize=1,MaxLODSize=256,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_VehicleNormalMap=(MinLODSize=1,MaxLODSize=256,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_VehicleSpecular=(MinLODSize=1,MaxLODSize=256,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_Weapon=(MinLODSize=1,MaxLODSize=64,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_WeaponNormalMap=(MinLODSize=1,MaxLODSize=64,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_WeaponSpecular=(MinLODSize=1,MaxLODSize=64,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_World=(MinLODSize=1,MaxLODSize=2,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_WorldNormalMap=(MinLODSize=1,MaxLODSize=2,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_WorldSpecular=(MinLODSize=1,MaxLODSize=2,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=bDisablePhysXHardwareSupport=True
+CVars=bFirstRun=False
+CVars=bSmoothFrameRate=true
+CVars=r.AOTrimOldRecordsFraction=0
+CVars=r.AmbientOcclusionLevels=0
+CVars=r.Atmosphere=0
+CVars=r.BloomQuality=0
+CVars=r.ClearWithExcludeRects=0
+CVars=r.CompileShadersForDevelopment=0
;+CVars=r.CustomDepth=0 ;outlines
+CVars=r.DefaultFeature.AmbientOcclusion=False
+CVars=r.DefaultFeature.AntiAliasing=0
+CVars=r.DefaultFeature.AutoExposure=False
+CVars=r.DefaultFeature.Bloom=False
+CVars=r.DefaultFeature.LensFlare=False
+CVars=r.DefaultFeature.MotionBlur=False
+CVars=r.DepthOfFieldQuality=0
+CVars=r.DetailMode=0
+CVars=r.EarlyZPass=0
+CVars=r.ExposureOffset=0.3
+CVars=r.HZBOcclusion=0
+CVars=r.LensFlareQuality=0
+CVars=r.LightFunctionQuality=0
+CVars=r.LightShaftQuality=0
+CVars=r.LightShafts=0
+CVars=r.MaxAnisotropy=0
+CVars=r.MotionBlurQuality=0
+CVars=r.PostProcessAAQuality=0
+CVars=r.ReflectionEnvironment=0
+CVars=r.RefractionQuality=0
+CVars=r.SSAOSmartBlur=0
+CVars=r.SSR.Quality=0
+CVars=r.SSS.SampleSet=0
+CVars=r.SSS.Scale=0
+CVars=r.SceneColorFringe.Max=0
+CVars=r.SceneColorFringeQuality=0
+CVars=r.Shadow.CSM.MaxCascades=1
+CVars=r.Shadow.CSM.TransitionScale=0
+CVars=r.Shadow.DistanceScale=0.1
+CVars=r.Shadow.MaxResolution=2
+CVars=r.Shadow.MinResolution=2
+CVars=r.Shadow.RadiusThreshold=0.1
+CVars=r.ShadowQuality=0
+CVars=r.TonemapperQuality=0
+CVars=r.TriangleOrderOptimization=1
+CVars=r.TrueSkyQuality=0
+CVars=r.UpsampleQuality=0
+CVars=r.ViewDistanceScale=0
+CVars=r.oneframethreadlag=1
+CVars=ShowFlag.LightFunctions=1
+CVars=t.maxfps=165


[WindowsNoEditor DeviceProfile]
DeviceType=WindowsNoEditor
BaseProfileName=Windows

[WindowsServer DeviceProfile]
DeviceType=WindowsServer
BaseProfileName=Windows

[IOS DeviceProfile]
DeviceType=IOS
BaseProfileName=
+CVars=r.BloomQuality=0
+CVars=r.DepthOfFieldQuality=0
+CVars=r.LightShaftQuality=0
+CVars=r.RefractionQuality=0

[iPad2 DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.RenderTargetSwitchWorkaround=1

[iPad3 DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.RenderTargetSwitchWorkaround=1

[iPad4 DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.RenderTargetSwitchWorkaround=1

[iPadAir DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.BloomQuality=1

[iPadMini DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.RenderTargetSwitchWorkaround=1

[iPadMini2 DeviceProfile]
DeviceType=IOS
BaseProfileName=iPadAir

[iPhone4 DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.RenderTargetSwitchWorkaround=1

[iPhone4S DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.RenderTargetSwitchWorkaround=1

[iPhone5 DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.RenderTargetSwitchWorkaround=1

[iPhone5S DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.MobileContentScaleFactor=2
+CVars=r.BloomQuality=1
+CVars=r.DepthOfFieldQuality=1
+CVars=r.LightShaftQuality=1

[iPodTouch5 DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.RenderTargetSwitchWorkaround=1

[iPhone6 DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.MobileContentScaleFactor=0
+CVars=r.BloomQuality=1
+CVars=r.DepthOfFieldQuality=1
+CVars=r.LightShaftQuality=1

[iPhone6Plus DeviceProfile]
DeviceType=IOS
BaseProfileName=IOS
+CVars=r.MobileContentScaleFactor=0
+CVars=r.BloomQuality=1
+CVars=r.DepthOfFieldQuality=1
+CVars=r.LightShaftQuality=1

[Android DeviceProfile]
DeviceType=Android
BaseProfileName=
+CVars=r.MobileContentScaleFactor=1
+CVars=r.BloomQuality=0
+CVars=r.DepthOfFieldQuality=0
+CVars=r.LightShaftQuality=0
+CVars=r.RefractionQuality=0

[Android_Low DeviceProfile]
DeviceType=Android
BaseProfileName=Android
+CVars=r.MobileContentScaleFactor=0.5

[Android_Mid DeviceProfile]
DeviceType=Android
BaseProfileName=Android
+CVars=r.BloomQuality=1
+CVars=r.MobileContentScaleFactor=0.8

[Android_High DeviceProfile]
DeviceType=Android
BaseProfileName=Android
+CVars=r.BloomQuality=1
+CVars=r.DepthOfFieldQuality=1
+CVars=r.LightShaftQuality=1
+CVars=r.MobileContentScaleFactor=1.0

[Android_Unrecognized DeviceProfile]
DeviceType=Android
BaseProfileName=Android_Mid

[Android_Adreno320 DeviceProfile]
DeviceType=Android
BaseProfileName=Android_Mid

;This offset needs to be set for the mosaic fallback to work on Galaxy S4 (SAMSUNG-IGH-I337)
;+CVars=r.DemosaicVposOffset=0.5

[Android_Adreno330 DeviceProfile]
DeviceType=Android
BaseProfileName=Android_High

[Android_Adreno330_Ver53 DeviceProfile]
DeviceType=Android
BaseProfileName=Android_Adreno330
+CVars=r.DisjointTimerQueries=1

[PS4 DeviceProfile]
DeviceType=PS4
BaseProfileName=

[XboxOne DeviceProfile]
DeviceType=XboxOne
BaseProfileName=
; we output 10:10:10, not 8:8:8 so we don't need color quantization
+CVars=r.TonemapperQuality=0
; For SSAO we rely on TemporalAA (with a randomized sample pattern over time) so we can use less samples
+CVars=r.AmbientOcclusionSampleSetQuality=0
; less passes, and no upsampling as even upsampling costs some performance
+CVars=r.AmbientOcclusionLevels=1
; larger radius to compensate for fewer passes
+CVars=r.AmbientOcclusionRadiusScale=2


[HTML5 DeviceProfile]
DeviceType=HTML5
BaseProfileName=
+CVars=r.RefractionQuality=0

[Mac DeviceProfile]
DeviceType=Mac
BaseProfileName=

[MacNoEditor DeviceProfile]
DeviceType=MacNoEditor
BaseProfileName=Mac

[MacServer DeviceProfile]
DeviceType=MacServer
BaseProfileName=Mac

[WinRT DeviceProfile]
DeviceType=WinRT
BaseProfileName=

[Linux DeviceProfile]
DeviceType=Linux
BaseProfileName=
MeshLODSettings=
TextureLODSettings=

[LinuxNoEditor DeviceProfile]
DeviceType=LinuxNoEditor
BaseProfileName=Linux
MeshLODSettings=
TextureLODSettings=

[LinuxServer DeviceProfile]
DeviceType=LinuxServer
BaseProfileName=Linux
MeshLODSettings=
TextureLODSettings=
""",
    }
    
    @staticmethod
    def get_config(config_type="DEFAULT", spyglass_fix=False):
        """Get the appropriate config based on selections"""
        if config_type == "DEFAULT":
            return ConfigManager.CONFIGS.get("DEFAULT", "")
        elif config_type == "HARD":
            return ConfigManager.CONFIGS.get("HARD", "")
        
        # For PVP configs
        if spyglass_fix:
            return ConfigManager.CONFIGS.get("PVP_SPYGLASS", "")
        else:
            return ConfigManager.CONFIGS.get("PVP", "")


class SettingsManager:
    """Manages application settings"""
    
    @staticmethod
    def load_settings():
        """Load settings from config file"""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    @staticmethod
    def save_settings(settings):
        """Save settings to config file"""
        os.makedirs(APPDATA_FOLDER, exist_ok=True)
        with open(CONFIG_FILE, 'w') as f:
            json.dump(settings, f, indent=4)
    
    @staticmethod
    def detect_ark_path():
        """Smart auto-detect: Search all drives for Steam/SteamLibrary/ARK"""
        import ctypes
        
        print("Starting smart auto-detect across all drives...", flush=True)
        
        # Get all available drives (local fixed disks only)
        drives = []
        for letter in string.ascii_uppercase:
            drive = f"{letter}:\\"
            if os.path.exists(drive):
                try:
                    # Get drive type (2=removable, 3=local fixed, 4=network, 5=cd)
                    drive_type = ctypes.windll.kernel32.GetDriveTypeW(drive)
                    
                    # Only include local fixed disks (type 3)
                    if drive_type == 3:
                        print(f"Checking local disk: {drive}", flush=True)
                        drives.append(drive)
                    else:
                        print(f"Skipping drive {drive} (not a local fixed disk)", flush=True)
                        
                except:
                    # If any error, skip this drive
                    continue
        
        print(f"Valid local disks to search: {', '.join(drives)}", flush=True)
        
        steam_patterns = [
            "Steam\\steamapps\\common\\ARK",
            "SteamLibrary\\steamapps\\common\\ARK",
            "Program Files (x86)\\Steam\\steamapps\\common\\ARK",
            "Program Files (x86)\\SteamLibrary\\steamapps\\common\\ARK",
            "Program Files\\Steam\\steamapps\\common\\ARK",
            "Program Files\\SteamLibrary\\steamapps\\common\\ARK",
        ]
        
        # Search each drive
        for drive in drives:
            for pattern in steam_patterns:
                ark_path = os.path.join(drive, pattern)
                config_file = os.path.join(ark_path, "Engine", "Config", "BaseDeviceProfiles.ini")
                
                if os.path.exists(config_file):
                    print(f"Found Ark at: {ark_path}", flush=True)
                    return ark_path
        
        print("Ark installation not found on any drive", flush=True)
        return None


class ArkConfigApp:
    """Main application with dark mode UI"""
    
    def __init__(self, root):
        self.root = root
        # Set window icon
        try:
            # For .exe, PyInstaller bundles the icon
            import sys
            import os
            if hasattr(sys, '_MEIPASS'):
                # Running as .exe
                icon_path = os.path.join(sys._MEIPASS, 'icon.ico')
            else:
                # Running as .py
                icon_path = 'icon.ico'
            self.root.iconbitmap(icon_path)
        except:
            pass
        self.root.title("Ark Config Switcher")
        self.root.geometry("800x720")
        self.root.resizable(False, False)
        
        # Dark mode background
        self.root.configure(bg=DARK_BG)
        
        # Force to front
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after(100, lambda: self.root.attributes('-topmost', False))
        
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.root.winfo_screenheight() // 2) - (720 // 2)
        self.root.geometry(f"800x720+{x}+{y}")
        
        # Configure dark mode style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('Dark.TSeparator', background='#404040')
        
        # Container for switching views
        self.container = tk.Frame(self.root, bg=DARK_BG)
        self.container.pack(fill=tk.BOTH, expand=True)
        
        # Load settings
        settings = SettingsManager.load_settings()
        self.ark_path = settings.get("ark_path")
        
        # Show appropriate screen
        if not self.ark_path or not os.path.exists(self.ark_path):
            self.show_setup_screen()
        else:
            self.show_main_screen()
    
    def clear_container(self):
        """Clear all widgets from container"""
        for widget in self.container.winfo_children():
            widget.destroy()
    
    def show_setup_screen(self):
        """Show setup screen with dark mode"""
        self.clear_container()
        
        # Title
        title = tk.Label(
            self.container,
            text="Welcome to Ark Config Switcher!",
            font=("Segoe UI", 22, "bold"),
            bg=DARK_BG,
            fg=DARK_FG
        )
        title.pack(pady=40)
        
        # Description
        desc = tk.Label(
            self.container,
            text="Select your Ark: Survival Evolved installation folder\n(The main ARK folder, not a subfolder)",
            font=("Segoe UI", 11),
            justify=tk.CENTER,
            bg=DARK_BG,
            fg=DARK_FG
        )
        desc.pack(pady=10)
        
        # Example path
        example = tk.Label(
            self.container,
            text='Example: D:\\Steam\\steamapps\\common\\ARK',
            font=("Segoe UI", 10, "italic"),
            bg=DARK_BG,
            fg="#888888"
        )
        example.pack(pady=5)
        
        # Info about auto-detect
        info_frame = tk.Frame(self.container, bg="#2d2d30", relief=tk.FLAT, bd=1)
        info_frame.pack(pady=20, padx=60, fill=tk.X)
        
        info_icon = tk.Label(
            info_frame,
            text="INFO",
            font=("Segoe UI", 11, "bold"),
            bg="#2d2d30",
            fg=ACCENT_BLUE
        )
        info_icon.pack(side=tk.LEFT, padx=(15, 10), pady=10)
        
        info = tk.Label(
            info_frame,
            text="Auto-Detect will scan all drives for Steam installations",
            font=("Segoe UI", 10),
            bg="#2d2d30",
            fg=INPUT_FG,
            justify=tk.LEFT
        )
        info.pack(side=tk.LEFT, pady=10, padx=(0, 15))
        
        # Path frame
        path_label = tk.Label(
            self.container,
            text="Ark Installation Path:",
            font=("Segoe UI", 10, "bold"),
            bg=DARK_BG,
            fg=DARK_FG,
            anchor=tk.W
        )
        path_label.pack(padx=60, pady=(20, 5), fill=tk.X)
        
        path_frame = tk.Frame(self.container, bg=DARK_BG)
        path_frame.pack(pady=5, padx=60, fill=tk.X)
        
        self.path_var = tk.StringVar()
        path_entry = tk.Entry(
            path_frame,
            textvariable=self.path_var,
            font=("Segoe UI", 11),
            bg=INPUT_BG,
            fg=INPUT_FG,
            insertbackground=INPUT_FG,
            relief=tk.FLAT,
            bd=5
        )
        path_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, ipady=8)
        
        browse_btn = tk.Button(
            path_frame,
            text="Browse",
            command=self.browse_path,
            font=("Segoe UI", 10, "bold"),
            bg=BUTTON_BG,
            fg=DARK_FG,
            activebackground=BUTTON_HOVER,
            activeforeground=DARK_FG,
            relief=tk.FLAT,
            bd=0,
            padx=20,
            cursor="hand2"
        )
        browse_btn.pack(side=tk.RIGHT, padx=(10, 0), ipady=8)
        
        # Auto-detect button
        auto_btn = tk.Button(
            self.container,
            text="Auto-Detect Ark Installation",
            command=self.auto_detect,
            font=("Segoe UI", 13, "bold"),
            bg=ACCENT_BLUE,
            fg="white",
            activebackground="#0a5a5d",
            activeforeground="white",
            relief=tk.FLAT,
            bd=0,
            padx=30,
            pady=15,
            cursor="hand2"
        )
        auto_btn.pack(pady=20)
        
        # Continue button
        continue_btn = tk.Button(
            self.container,
            text="Continue",
            command=self.validate_and_continue,
            font=("Segoe UI", 13, "bold"),
            bg=ACCENT_GREEN,
            fg="white",
            activebackground="#1e4d35",
            activeforeground="white",
            relief=tk.FLAT,
            bd=0,
            padx=40,
            pady=15,
            cursor="hand2"
        )
        continue_btn.pack(pady=10)
    
    def browse_path(self):
        path = filedialog.askdirectory(title="Select Ark Installation Folder (main ARK folder)")
        if path:
            self.path_var.set(path)
    
    def auto_detect(self):
        # Update UI to show searching
        self.root.config(cursor="wait")
        self.root.update()
        
        detected = SettingsManager.detect_ark_path()
        
        self.root.config(cursor="")
        
        if detected:
            self.path_var.set(detected)
            messagebox.showinfo(
                "Success!",
                f"Ark installation found!\n\n{detected}",
                parent=self.root
            )
        else:
            messagebox.showwarning(
                "Not Found",
                "Could not find Ark installation on any drive.\n\n"
                "Please browse to your main ARK folder manually.\n"
                "(e.g., D:\\Steam\\steamapps\\common\\ARK)",
                parent=self.root
            )
    
    def validate_and_continue(self):
        path = self.path_var.get()
        if not path:
            messagebox.showerror("Error", "Please select a path first.", parent=self.root)
            return
        
        if not os.path.exists(path):
            messagebox.showerror("Error", "The selected path does not exist.", parent=self.root)
            return
        
        # Check if Engine/Config folder exists
        config_path = os.path.join(path, "Engine", "Config", "BaseDeviceProfiles.ini")
        if not os.path.exists(config_path):
            result = messagebox.askyesno(
                "Warning",
                f"Could not find Engine\\Config\\BaseDeviceProfiles.ini\n\n"
                f"Selected: {path}\n\n"
                "This might not be the correct ARK folder. Continue anyway?",
                parent=self.root
            )
            if not result:
                return
        
        # Save settings
        self.ark_path = path
        settings = {"ark_path": path}
        SettingsManager.save_settings(settings)
        
        # Go to main screen
        self.show_main_screen()
    
    def show_main_screen(self):
        """Show main application screen with dark mode"""
        self.clear_container()
        
        # Variables
        self.config_type = tk.StringVar(value="DEFAULT")
        self.spyglass_var = tk.BooleanVar(value=False)
        
        # Header - increased height slightly to prevent text cutoff
        header = tk.Frame(self.container, bg=DARK_HEADER, height=65)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title = tk.Label(
            header,
            text="Ark: SE Config Switcher",
            font=("Segoe UI", 24, "bold"),
            bg=DARK_HEADER,
            fg=DARK_FG
        )
        title.pack(pady=10)
        
        # Main content
        content = tk.Frame(self.container, bg=DARK_BG, padx=50, pady=25)
        content.pack(fill=tk.BOTH, expand=True)
        
        # Current path display - fixed icon alignment
        path_frame = tk.Frame(content, bg="#2d2d30", relief=tk.FLAT)
        path_frame.pack(fill=tk.X, pady=(0, 25))
        
        path_container = tk.Frame(path_frame, bg="#2d2d30")
        path_container.pack(padx=15, pady=10, fill=tk.X)
        
        path_icon = tk.Label(
            path_container,
            text="FOLDER:",
            font=("Segoe UI", 9, "bold"),
            bg="#2d2d30",
            fg="#888888"
        )
        path_icon.pack(side=tk.LEFT, padx=(0, 8))
        
        path_text = tk.Label(
            path_container,
            text=self.ark_path,
            font=("Segoe UI", 9),
            bg="#2d2d30",
            fg="#888888",
            anchor=tk.W
        )
        path_text.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Config selection
        config_label = tk.Label(
            content,
            text="Configuration Type:",
            font=("Segoe UI", 13, "bold"),
            bg=DARK_BG,
            fg=DARK_FG,
            anchor=tk.W
        )
        config_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Radio buttons for config type
        radio_frame = tk.Frame(content, bg=DARK_BG)
        radio_frame.pack(anchor=tk.W, fill=tk.X, padx=15)
        
        default_radio = tk.Radiobutton(
            radio_frame,
            text="Default Configuration",
            variable=self.config_type,
            value="DEFAULT",
            font=("Segoe UI", 11),
            bg=DARK_BG,
            fg=DARK_FG,
            selectcolor=BUTTON_BG,
            activebackground=DARK_BG,
            activeforeground=DARK_FG,
            command=self.update_fix_visibility,
            cursor="hand2"
        )
        default_radio.pack(anchor=tk.W, pady=6)
        
        default_desc = tk.Label(
            radio_frame,
            text="Standard Ark settings (vanilla game)",
            font=("Segoe UI", 9),
            bg=DARK_BG,
            fg="#888888",
            anchor=tk.W
        )
        default_desc.pack(anchor=tk.W, padx=25, pady=(0, 8))
        
        pvp_radio = tk.Radiobutton(
            radio_frame,
            text="PVP Configuration",
            variable=self.config_type,
            value="PVP",
            font=("Segoe UI", 11),
            bg=DARK_BG,
            fg=DARK_FG,
            selectcolor=BUTTON_BG,
            activebackground=DARK_BG,
            activeforeground=DARK_FG,
            command=self.update_fix_visibility,
            cursor="hand2"
        )
        pvp_radio.pack(anchor=tk.W, pady=6)
        
        pvp_desc = tk.Label(
            radio_frame,
            text="Optimized for PVP gameplay with performance enhancements",
            font=("Segoe UI", 9),
            bg=DARK_BG,
            fg="#888888",
            anchor=tk.W
        )
        pvp_desc.pack(anchor=tk.W, padx=25, pady=(0, 8))
        
        hard_radio = tk.Radiobutton(
            radio_frame,
            text="HARD Configuration",
            variable=self.config_type,
            value="HARD",
            font=("Segoe UI", 11),
            bg=DARK_BG,
            fg=DARK_FG,
            selectcolor=BUTTON_BG,
            activebackground=DARK_BG,
            activeforeground=DARK_FG,
            command=self.update_fix_visibility,
            cursor="hand2"
        )
        hard_radio.pack(anchor=tk.W, pady=6)
        
        hard_desc = tk.Label(
            radio_frame,
            text="Extreme INI mainly for hardcore PVP. Disables pretty much everything in the way",
            font=("Segoe UI", 9),
            bg=DARK_BG,
            fg="#888888",
            anchor=tk.W
        )
        hard_desc.pack(anchor=tk.W, padx=25, pady=(0, 5))
        
        # Separator
        separator = ttk.Separator(content, orient=tk.HORIZONTAL, style='Dark.TSeparator')
        separator.pack(fill=tk.X, pady=25)
        
        # Fixes section - ABOVE buttons
        self.fixes_frame = tk.Frame(content, bg=DARK_BG)
        self.fixes_frame.pack(fill=tk.X, pady=(0, 20))
        
        fixes_label = tk.Label(
            self.fixes_frame,
            text="Optional Fixes:",
            font=("Segoe UI", 13, "bold"),
            bg=DARK_BG,
            fg=DARK_FG,
            anchor=tk.W
        )
        fixes_label.pack(anchor=tk.W, pady=(0, 15))
        
        # Spyglass fix - checkbox and name on same line, description below
        spyglass_container = tk.Frame(self.fixes_frame, bg=DARK_BG)
        spyglass_container.pack(fill=tk.X, pady=8, padx=15)
        
        self.spyglass_check = tk.Checkbutton(
            spyglass_container,
            text="Awesome Spyglass Outline Fix",
            variable=self.spyglass_var,
            font=("Segoe UI", 11, "bold"),
            bg=DARK_BG,
            fg=DARK_FG,
            selectcolor=BUTTON_BG,
            activebackground=DARK_BG,
            activeforeground=DARK_FG,
            cursor="hand2"
        )
        self.spyglass_check.pack(anchor=tk.W)
        
        spyglass_desc = tk.Label(
            spyglass_container,
            text="Fixes outline rendering issues with the Awesome Spyglass mod. Enables proper display of outlines.\n(Little to no performance impact)",
            font=("Segoe UI", 9),
            bg=DARK_BG,
            fg="#888888",
            justify=tk.LEFT,
            anchor=tk.W,
            wraplength=650
        )
        spyglass_desc.pack(anchor=tk.W, padx=25, pady=(3, 0))
        
        # Button frame at BOTTOM
        button_frame = tk.Frame(content, bg=DARK_BG)
        button_frame.pack(side=tk.BOTTOM, pady=2)
        
        apply_btn = tk.Button(
            button_frame,
            text="Apply Configuration",
            command=self.apply_config,
            font=("Segoe UI", 13, "bold"),
            bg=ACCENT_GREEN,
            fg="white",
            activebackground="#1e4d35",
            activeforeground="white",
            relief=tk.FLAT,
            bd=0,
            padx=35,
            pady=15,
            cursor="hand2"
        )
        apply_btn.pack(side=tk.LEFT, padx=10)
        
        settings_btn = tk.Button(
            button_frame,
            text="Change Path",
            command=self.show_setup_screen,
            font=("Segoe UI", 12, "bold"),
            bg=ACCENT_ORANGE,
            fg="white",
            activebackground="#b45309",
            activeforeground="white",
            relief=tk.FLAT,
            bd=0,
            padx=30,
            pady=15,
            cursor="hand2"
        )
        settings_btn.pack(side=tk.LEFT, padx=10)
        
        self.update_fix_visibility()
    
    def update_fix_visibility(self):
        """Show/hide fix options based on config type"""
        if self.config_type.get() == "PVP":
            self.fixes_frame.pack(fill=tk.X, pady=(0, 20))
        else:
            self.fixes_frame.pack_forget()
    
    def apply_config(self):
        """Apply the selected configuration"""
        try:
            # Get the appropriate config
            config_content = ConfigManager.get_config(
                config_type=self.config_type.get(),
                spyglass_fix=self.spyglass_var.get()
            )
            
            if not config_content:
                messagebox.showerror(
                    "Error",
                    "Configuration content is empty.\nConfig files may not be loaded.",
                    parent=self.root
                )
                return
            
            # Target file path - Engine/Config/BaseDeviceProfiles.ini
            target_file = os.path.join(self.ark_path, "Engine", "Config", "BaseDeviceProfiles.ini")
            
            # Verify directory exists
            target_dir = os.path.dirname(target_file)
            if not os.path.exists(target_dir):
                messagebox.showerror(
                    "Error",
                    f"Config directory not found:\n{target_dir}\n\n"
                    "Please verify your Ark installation path.",
                    parent=self.root
                )
                return
            
            # Write new config (no backup as requested)
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(config_content)
            
            # Build success message
            config_names = {
                "DEFAULT": "Default",
                "PVP": "PVP",
                "HARD": "HARD"
            }
            config_name = config_names.get(self.config_type.get(), "Unknown")
            fixes = []
            if self.config_type.get() == "PVP":
                if self.spyglass_var.get():
                    fixes.append("Spyglass Fix")
            
            msg = f"Configuration applied successfully!\n\n"
            
            messagebox.showinfo("Success", msg, parent=self.root)
            
        except PermissionError:
            messagebox.showerror(
                "Permission Error",
                "Could not write to the config file.\n\n"
                "Try running this application as Administrator.",
                parent=self.root
            )
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Failed to apply configuration:\n{str(e)}",
                parent=self.root
            )


def main():
    print("="*60, flush=True)
    print("Ark Config Switcher - Starting...", flush=True)
    print(f"Settings location: {APPDATA_FOLDER}", flush=True)
    print(f"Configs loaded: {len(ConfigManager.CONFIGS)}/4", flush=True)
    print("="*60, flush=True)
    
    root = tk.Tk()
    app = ArkConfigApp(root)
    
    print("Application window created", flush=True)
    root.mainloop()
    print("Application closed", flush=True)


if __name__ == "__main__":
    main()
