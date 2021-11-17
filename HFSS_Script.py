from win32com import client
import numpy
import Meta_Generator
import os


class HFSS:
    def __init__(self, _pj_name = None):
        self.oAnsoftApp = client.Dispatch('AnsoftHfss.HfssScriptInterface')
        # if _pj_name == None:
        self.oDesktop = self.oAnsoftApp.GetAppDesktop()
        self.oProject = self.oDesktop.NewProject(_pj_name)

    def new_design(self, _design_name):
        self.oProject.InsertDesign('HFSS', _design_name, 'DrivenModal1', '')
        self.oDesign = self.oProject.SetActiveDesign(_design_name)
        self.oEditor = self.oDesign.SetActiveEditor("3D Modeler")
        self.oModule = self.oDesign.GetModule('BoundarySetup')
        self.transparency = 0.5

    def delete_design(self, _design_name):
        self.oProject.DeleteDesign(_design_name)

    def delete_project(self, _project_name):
        str_name = self.oDesktop.GetProjects()
        pj_name = str_name(_project_name)
        self.oDesktop.DeleteProject(pj_name)


    def set_variable(self, _var_name, _var_value, _unit=""):
        _NAME = 'NAME:' + _var_name
        _VALUE = str(_var_value) + _unit
        self.oDesign.ChangeProperty(
        [
            "NAME:AllTabs",
            [
                "NAME:LocalVariableTab",
                [
                    "NAME:PropServers",
                    "LocalVariables"
                ],
                [
                    "NAME:NewProps",
                    [
                        'NAME:' + _var_name,
                        "PropType:="	, "VariableProp",
                        "UserDef:="		, True,
                        "Value:="		, str(_var_value) + _unit
                    ]
                ]
            ]
        ])

    def create_centered_rectangle(self, _var_x, _var_y, _var_z, _name, _dir='Z'):
        self.oEditor.CreateRectangle(
            [
                "NAME:RectangleParameters",
                "IsCovered:=", True,
                "XStart:="	, '-' + _var_x + '/2',
                "YStart:="		, '-' + _var_y + '/2',
                "ZStart:="		, _var_z,
                "Width:="		, _var_x,
                "Height:="		, _var_y,
                "WhichAxis:="		, _dir
            ],
            [
                "NAME:Attributes",
                "Name:="		, _name,
                "Flags:="		, "",
                "Color:="		, "(143 175 143)",
                "Transparency:="	, 0,
                "PartCoordinateSystem:=", "Global",
                "UDMId:="		, "",
                "MaterialValue:="	, "\"vacuum\"",
                "SurfaceMaterialValue:=", "\"\"",
                "SolveInside:="		, True,
                "IsMaterialEditable:="	, True,
                "UseMaterialAppearance:=", False
            ])

    def connect(self, _obj1, _obj2):
        self.oEditor.Connect(["NAME:Selections", "Selections:=", _obj1 + ',' + _obj2])

    def unite(self, _obj1, _obj2):
        self.oEditor.Unite(["NAME:Selections", "Selections:=", _obj1 + ',' + _obj2],
                           ["NAME:UniteParameters", "KeepOriginals:=", False])

    def rotation(self, _obj1, theta):
        self.oEditor.Roate(["NAME:Selections", "Selections:=", _obj1],
                           ["NAME:RotateParameters",
                            "RotateAxis:=", "Z"  ,
                            "RotateAngle:=", theta] )


    def move(self, _obj1, dx, dy, dz):

        self.oEditor.Roate(["NAME:Selections", "Selections:=", _obj1],
                           ["NAME:TranslateParameters",
                            "TranslateVectorX:=", dx,
                            "TranslateVectorY:=", dy,
                            "TranslateVectorZ:=", dz]
        )



    def duplicate_mirror(self, _obj, plane ):
        if plane == 'xy':
            _x = 0
            _y = 0
            _z = 1

        elif plane == 'yz':
            _x = 1
            _y = 0
            _z = 0
        else:
            _x = 0
            _y = 1
            _z = 0

        self.oEditor.DuplicateMirror(
            [
                "NAME:Selections",
                "Selections:="	, _obj,
                "NewPartsModelFlag:="	, "Model"
            ],
            [
                "NAME:DuplicateToMirrorParameters",
                "DuplicateMirrorBaseX:=", "0mm",
                "DuplicateMirrorBaseY:=", "0mm",
                "DuplicateMirrorBaseZ:=", "0mm",
                "DuplicateMirrorNormalX:=", str(_x)+"mm",
                "DuplicateMirrorNormalY:=", str(_y)+"mm",
                "DuplicateMirrorNormalZ:=", str(_z)+"mm"
            ],
            [
                "NAME:Options",
                "DuplicateAssignments:=", False
            ],
            )

    def subtract(self, _obj1, _obj2):
        self.oEditor.Subtract(["NAME:Selections", "Blank Parts:=", _obj1, "Tool Parts:=", _obj2],
                              ["NAME:SubtractParameters", "KeepOriginals:=", False])

    def copy_and_paste(self, _obj):
        self.oEditor.Copy(["NAME:Selections", "Selections:=", _obj])
        self.oEditor.Paste()

    def set_material(self, _obj, _mat='pec'):
        self.oEditor.AssignMaterial(
            [
                "NAME:Selections",
                "AllowRegionDependentPartSelectionForPMLCreation:=", True,
                "AllowRegionSelectionForPMLCreation:=", True,
                "Selections:="	, _obj
            ],
            [
                "NAME:Attributes",
                "MaterialValue:="	, "\"" + _mat + "\"",
                "SolveInside:="		, False,
                "IsMaterialEditable:="	, True,
                "UseMaterialAppearance:=", False
            ])

    def assign_port(self, _obj):
        self.oModule.AssignWavePort(["NAME:1", "Objects:=", [_obj],
                                     "NumModes:=", 1, "RenormalizeAllTerminals:=", True,
                                     "UseLineModeAlignment:=", False, "DoDeembed:="	, False,
                                     ["NAME:Modes",
                                      ["NAME:Mode1", "ModeNum:=", 1, "UseIntLine:=", False, "CharImp:=", "Zpi"]],
                                     "ShowReporterFilter:="	, False,
                                     "ReporterFilter:="	, [True],
                                     "UseAnalyticAlignment:=", False])

    def create_region(self, _var_ab):
        self.oEditor.CreateRegion(
            [
                "NAME:RegionParameters",
                "+XPaddingType:="	, "Absolute Offset",
                "+XPadding:="		, _var_ab,
                "-XPaddingType:="	, "Absolute Offset",
                "-XPadding:="		, _var_ab,
                "+YPaddingType:="	, "Absolute Offset",
                "+YPadding:="		, _var_ab,
                "-YPaddingType:="	, "Absolute Offset",
                "-YPadding:="		, _var_ab,
                "+ZPaddingType:="	, "Absolute Offset",
                "+ZPadding:="		, _var_ab,
                "-ZPaddingType:="	, "Absolute Offset",
                "-ZPadding:="		, _var_ab
            ],
            [
                "NAME:Attributes",
                "Name:="		, "Region",
                "Flags:="		, "Wireframe#",
                "Color:="		, "(143 175 143)",
                "Transparency:="	, 0,
                "PartCoordinateSystem:=", "Global",
                "UDMId:="		, "",
                "MaterialValue:="	, "\"vacuum\"",
                "SurfaceMaterialValue:=", "\"\"",
                "SolveInside:="		, True,
                "IsMaterialEditable:="	, True,
                "UseMaterialAppearance:=", False
            ])

    def assign_radiation_region(self):
        self.oModule.AssignRadiation(
            [
                "NAME:Rad1",
                "Objects:="		, ["Region"],
                "IsFssReference:="	, False,
                "IsForPML:="		, False
            ])

    def insert_radiation_setup(self):
        mod = self.oDesign.GetModule('RadField')
        mod.InsertFarFieldSphereSetup(
            [
                "NAME:Infinite Sphere1",
                "UseCustomRadiationSurface:=", False,
                "ThetaStart:="		, "-180deg",
                "ThetaStop:="		, "180deg",
                "ThetaStep:="		, "1deg",
                "PhiStart:="		, "0deg",
                "PhiStop:="		, "90deg",
                "PhiStep:="		, "90deg",
                "UseLocalCS:="		, False
            ])

    def insert_analysis_setup(self, _opj, _fs, _fe):
        mod = self.oDesign.GetModule('AnalysisSetup')
        mod.InsertSetup("HfssDriven",
                        [
                            "NAME:"+_opj,
                            "AdaptMultipleFreqs:="	, True,
                            [
                                "NAME:MultipleAdaptiveFreqsSetup",
                                [
                                    "NAME:Broadband",
                                    "Low:="			, str(_fs) +"GHz",
                                    "High:="		, str(_fe) +"GHz"
                                ]
                            ],
                            "MaxDeltaS:="		, 0.02,
                            "MaximumPasses:="	, 20,
                            "MinimumPasses:="	, 2,
                            "MinimumConvergedPasses:=", 2,
                            "PercentRefinement:="	, 30,
                            "IsEnabled:="		, True,
                            "BasisOrder:="		, 1,
                            "DoLambdaRefine:="	, True,
                            "DoMaterialLambda:="	, True,
                            "SetLambdaTarget:="	, False,
                            "Target:="		, 0.3333,
                            "UseMaxTetIncrease:="	, False,
                            "PortAccuracy:="	, 2,
                            "UseABCOnPort:="	, False,
                            "SetPortMinMaxTri:="	, False,
                            "UseDomains:="		, False,
                            "UseIterativeSolver:="	, False,
                            "SaveRadFieldsOnly:="	, False,
                            "SaveAnyFields:="	, True,
                            "IESolverType:="	, "Auto",
                            "LambdaTargetForIESolver:=", 0.15,
                            "UseDefaultLambdaTgtForIESolver:=", True,
                            "RayDensityPerWavelength:=", 4,
                            "MaxNumberOfBounces:="	, 5,
                            "InfiniteSphereSetup:="	, -1
                        ])


    def insert_analysis_setup_old(self, _opj, _f_sol, _conv, _max_pass ):
        mod = self.oDesign.GetModule('AnalysisSetup')
        mod.InsertSetup("HfssDriven",
                        [
                            "NAME:"+_opj,
                            "Frequency:="	, str(_f_sol) +"GHz",
                            "PortsOnly:="		, False,
                            "MaxDeltaS:="		, _conv,
                            "UseMatrixConv:="	, False,
                            "MaximumPasses:="	, _max_pass,
                            "MinimumPasses:="	, 2,
                            "MinimumConvergedPasses:=", 1,
                            "PercentRefinement:="	, 30,
                            "IsEnabled:="		, True,
                            "BasisOrder:="		, 1,
                            "DoLambdaRefine:="	, True,
                            "DoMaterialLambda:="	, True,
                            "SetLambdaTarget:="	, False,
                            "Target:="		, 0.3333,
                            "UseMaxTetIncrease:="	, False,
                            "PortAccuracy:="	, 2,
                            "UseABCOnPort:="	, False,
                            "SetPortMinMaxTri:="	, False,
                            "UseDomains:="		, False,
                            "UseIterativeSolver:="	, False,
                            "SaveRadFieldsOnly:="	, False,
                            "SaveAnyFields:="	, True,
                            "IESolverType:="	, "Auto",
                            "LambdaTargetForIESolver:=", 0.15,
                            "UseDefaultLambdaTgtForIESolver:=", True
                        ])

    def insert_frequency_swap(self, _opj, _fs, _fe, _nfp ):
        mod = self.oDesign.GetModule('AnalysisSetup')
        mod.InsertFrequencySweep(_opj,
            [
                "NAME:Sweep",
                "IsEnabled:="		, True,
                "RangeType:="		, "LinearCount",
                "RangeStart:="		, str(_fs)+"GHz",
                "RangeEnd:="		, str(_fe)+"GHz",
                "RangeCount:="		, _nfp,
                "Type:="		, "Interpolating",
                "SaveFields:="		, False,
                "SaveRadFields:="	, False,
                "InterpTolerance:="	, 0.5,
                "InterpMaxSolns:="	, 250,
                "InterpMinSolns:="	, 0,
                "InterpMinSubranges:="	, 1,
                "ExtrapToDC:="		, False,
                "InterpUseS:="		, True,
                "InterpUsePortImped:="	, False,
                "InterpUsePropConst:="	, True,
                "UseDerivativeConvergence:=", False,
                "InterpDerivTolerance:=", 0.2,
                "UseFullBasis:="	, True,
                "EnforcePassivity:="	, True,
                "PassivityErrorTolerance:=", 0.0001
            ])

    def create_reports_tr(self, _st, _m):
        mod = self.oDesign.GetModule('ReportSetup')
        if(_m == 'phase'):_m='ang_deg'
        mod.CreateReport(_m+"_TR", "Modal Solution Data", "Rectangular Plot", _st+" : Sweep",
             ["Domain:=", "Sweep"],
             ["Freq:=", ["All"]],
             [
                 "X Component:="	, "Freq",
                 "Y Component:="		, [_m+"(S(FloquetPort1:1,FloquetPort1:1))" ,_m+"(S(FloquetPort1:1,FloquetPort1:2))" ,
                                           _m+"(S(FloquetPort1:1,FloquetPort2:1))" ,_m+"(S(FloquetPort1:1,FloquetPort2:2))"]
             ], [])

    def create_reports_tr_phase(self,_st):
        mod = self.oDesign.GetModule('ReportSetup')
        mod.CreateReport("Phase_TR", "Modal Solution Data", "Rectangular Plot", _st+" : Sweep",
             ["Domain:=", "Sweep"],
             ["Freq:=", ["All"]],
             [
                 "X Component:=", "Freq",
                 "Y Component:="		, ["ang_deg(S(FloquetPort1:1,FloquetPort1:1))","ang_deg(S(FloquetPort1:1,FloquetPort1:2))","ang_deg(S(FloquetPort1:1,FloquetPort2:1))","ang_deg(S(FloquetPort1:1,FloquetPort2:2))"]
             ], [])

    def create_reports_tr_ri(self, _st, my_path, _file_name="temp"):
        mod = self.oDesign.GetModule('ReportSetup')
        mod.CreateReport("RI_TR", "Modal Solution Data", "Data Table",  _st+" : Sweep",
             ["Domain:=", "Sweep"],
             ["Freq:=", ["All"]],
             [
                 "X Component:=", "Freq",
                 "Y Component:=", ["re(S(FloquetPort1:1,FloquetPort1:1))","im(S(FloquetPort1:1,FloquetPort1:1))","re(S(FloquetPort1:1,FloquetPort1:2))","im(S(FloquetPort1:1,FloquetPort1:2))","re(S(FloquetPort1:1,FloquetPort2:1))","im(S(FloquetPort1:1,FloquetPort2:1))","re(S(FloquetPort1:1,FloquetPort2:2))","im(S(FloquetPort1:1,FloquetPort2:2))"]
	         ], [])

        # my_path = os.path.abspath("./Res")
        # os.path.join(os.path.abspath("../Res"), _file_name + ".txt")
        my_path = my_path + _file_name + ".txt"
        # print(my_path)
        mod.ExportToFile("RI_TR", my_path)

    def save_prj(self):
        # _base_path = os.getcwd()
        _base_path = os.path.abspath("../Design")
        _prj_num = 1
        while True:
            _path = os.path.join(_base_path, 'Prj{}.aedt'.format(_prj_num))
            if os.path.exists(_path):
                _prj_num += 1
            else:
                break
        self.oProject.SaveAs(_path, True)

    def run(self, _opj):
        self.oDesktop.RestoreWindow()
        self.oDesign.Analyze(_opj)

    def create_box(self, _x, _y, _z, _dx, _dy, _dz, _name, _mat='vacuum' ):
        _Solve_Inside = False
        _Trans = 0.1
        if _mat == 'vacuum':
            _Solve_Inside = True
            _Trans = 0.99


        self.oEditor.CreateBox(
            [
                "NAME:BoxParameters",
                "XPosition:="	, _x,
                "YPosition:="	, _y,
                "ZPosition:="	, _z,
                "XSize:="		, _dx,
                "YSize:="		, _dy,
                "ZSize:="		, _dz
            ],
            [
                "NAME:Attributes",
                "Name:="		, _name,
                "Flags:="		, "",
                "Color:="		, "(143 175 143)",
                "Transparency:="	, _Trans,
                "PartCoordinateSystem:=", "Global",
                "UDMId:="		, "",
                "MaterialValue:="	, "\""+_mat+"\"",
                "SurfaceMaterialValue:=", "\"\"",

                "SolveInside:="		, _Solve_Inside,
                "IsMaterialEditable:="	, True
            ]
        )

    def create_cylinder(self, _x, _y, _z, _R, _h, _name, which_Ax = "Z", _mat='vacuum'):
        _Solve_Inside = False
        _Trans = 0.1
        if _mat == 'vacuum':
            _Solve_Inside = True
            _Trans = 0.99


        self.oEditor.CreateCylinder(
            [
                "NAME:CylinderParameters",
                "XCenter:=" 	, _x,
                "YCenter:="	    , _y,
                "ZCenter:="	    , _z,
                "Radius:="		, _R,
                "Height:="		, _h,
                "WhichAxis:="   , which_Ax
            ],
            [
                "NAME:Attributes",
                "Name:="		, _name,
                "Flags:="		, "",
                "Color:="		, "(143 175 143)",
                "Transparency:="	, _Trans,
                "PartCoordinateSystem:=", "Global",
                "UDMId:="		, "",
                "MaterialValue:="	, "\""+_mat+"\"",
                "SurfaceMaterialValue:=", "\"\"",

                "SolveInside:="		, _Solve_Inside,
                "IsMaterialEditable:="	, True
            ]
        )


    def create_box_Ellips(self, _x:float, _y:float, _z:float,
                         l1:float, l2:float, _dz:float,
                         _name:str, _mat='vacuum', which_Ax = "Z"):

        _Solve_Inside = False
        _Trans = 0.1
        if _mat == 'vacuum':
            _Solve_Inside = True
        _Trans = 0.99

        self.oEditor.CreateEllipse(
            [
                "NAME:CylinderParameters",
                "XCenter:="     , _x,
                "YCenter:="	    , _y,
                "ZCenter:="	    , _z,
                "MajRadius:="	, l1,
                "Ratio:="       , l1/l2,
                "WhichAxis:="   , which_Ax
            ],
            [
                "NAME:Attributes",
                "Name:=", _name,
                "Flags:="	, "",
                    "Color:="		, "(143 175 143)",
                    "Transparency:="	, 0,
                    "PartCoordinateSystem:=", "Global",
                    "UDMId:="		, "",
                    "MaterialValue:="	, "\"" +_mat + "\"",
                "SurfaceMaterialValue:=", "\"\"",
                "SolveInside:="	, _Solve_Inside,
                    "IsMaterialEditable:="	, True
                ])
        self.oEditor.SweepAlongVector(
            [
                "NAME:Selections",
                "Selections:="	, _name,
                "NewPartsModelFlag:="	, "Model"
            ],
            [
                "NAME:VectorSweepParameters",
                "DraftAngle:="		, "0deg",
                "DraftType:="		, "Round",
                "CheckFaceFaceIntersection:=", False,
                "SweepVectorX:="	, "0mm",
                "SweepVectorY:="	, "0mm",
                "SweepVectorZ:="	, str(_dz)+"mm"
            ])


    def create_box_trian(self, _x:float, _y:float, _z:float,
                         _dx:float, _dy:float, _dz:float, draw_type:int,
                         _name:str, _mat='vacuum'):

        _Solve_Inside = False
        _Trans = 0.1
        if _mat == 'vacuum':
            _Solve_Inside = True
            _Trans = 0.99

        if draw_type == 1:
            x1 = _x
            y1 = _y


            x2 = _x + _dx
            y2 = _y

            x3 = _x + _dx
            y3 = _y + _dy

        elif draw_type == 2:

            x1 = _x + _dx
            y1 = _y

            x2 = _x + _dx
            y2 = _y + _dy

            x3 = _x
            y3 = _y + _dy

        elif draw_type == 3:
            x1 = _x + _dx
            y1 = _y + _dy

            x2 = _x
            y2 = _y + _dy

            x3 = _x
            y3 = _y
        elif draw_type == 4:
            x1 = _x
            y1 = _y + _dy

            x2 = _x
            y2 = _y

            x3 = _x + _dx
            y3 = _y

        self.oEditor.CreatePolyline(
            [
                "NAME:PolylineParameters",
                "IsPolylineCovered:=", True,
                "IsPolylineClosed:=", True,
                [
                    "NAME:PolylinePoints",
                    [
                        "NAME:PLPoint",
                        "X:="		    , str(x1)+"mm",
                        "Y:="			, str(y1)+"mm",
                        "Z:="			, str(_z)+"mm"
                    ],
                    [
                        "NAME:PLPoint",
                        "X:="			, str(x2)+"mm",
                        "Y:="			, str(y2)+"mm",
                        "Z:="			, str(_z)+"mm"
                    ],
                    [
                        "NAME:PLPoint",
                        "X:="			, str(x3)+"mm",
                        "Y:="			, str(y3)+"mm",
                        "Z:="			, str(_z)+"mm"
                    ],
                    [
                        "NAME:PLPoint",
                        "X:="		    , str(x1)+"mm",
                        "Y:="			, str(y1)+"mm",
                        "Z:="			, str(_z)+"mm"
                    ]
                ],

                [
                    "NAME:PolylineSegments",
                    [
                        "NAME:PLSegment",
                        "SegmentType:="	, "Line",
                        "StartIndex:="		, 0,
                        "NoOfPoints:="		, 2
                    ],
                    [
                        "NAME:PLSegment",
                        "SegmentType:="		, "Line",
                        "StartIndex:="		, 1,
                        "NoOfPoints:="		, 2
                    ],
                    [
                        "NAME:PLSegment",
                        "SegmentType:="		, "Line",
                        "StartIndex:="		, 2,
                        "NoOfPoints:="		, 2
                    ]
                ],
                [
                    "NAME:PolylineXSection",
                    "XSectionType:=", "None",
                    "XSectionOrient:=", "Auto",
                    "XSectionWidth:=", "0mm",
                    "XSectionTopWidth:=", "0mm",
                    "XSectionHeight:=", "0mm",
                    "XSectionNumSegments:=", "0",
                    "XSectionBendType:=", "Corner"
                ]
            ],
            [
                "NAME:Attributes",
                "Name:="	, _name,
                "Flags:="		, "",
                "Color:="		, "(143 175 143)",
                "Transparency:="	, 0,
                "PartCoordinateSystem:=", "Global",
                "UDMId:="		, "",
                "MaterialValue:="	, "\"" +_mat +"\"",
                "SurfaceMaterialValue:=", "\"\"",
                "SolveInside:="		, _Solve_Inside,
                "IsMaterialEditable:="	, True
            ])
        self.oEditor.SweepAlongVector(
            [
                "NAME:Selections",
                "Selections:="	, _name,
                "NewPartsModelFlag:="	, "Model"
            ],
            [
                "NAME:VectorSweepParameters",
                "DraftAngle:="		, "0deg",
                "DraftType:="		, "Round",
                "CheckFaceFaceIntersection:=", False,
                "SweepVectorX:="	, "0mm",
                "SweepVectorY:="	, "0mm",
                "SweepVectorZ:="	, str(_dz)+"mm"
            ])
        # self.oEditor.AssignMaterial(
        #     [
        #         "NAME:Selections",
        #         "Selections:="		, _name,
        #     ],
        #     [
        #         "NAME:Attributes",
        #         "MaterialValue:="	, "\"" +_mat +"\"",
        #         "SolveInside:="		, _Solve_Inside,
        #         "IsMaterialEditable:="	, True
        #
        #     ])




    def create_pec_rectangle(self, _x, _y, _z, _var_x, _var_y, _name, _dir='Z'):
        self.oEditor.CreateRectangle(
            [
                "NAME:RectangleParameters",
                "IsCovered:=", True,
                "XStart:="	, _x,
                "YStart:="		, _y,
                "ZStart:="		, _z,
                "Width:="		, _var_x,
                "Height:="		, _var_y,
                "WhichAxis:="		, _dir
            ],
            [
                "NAME:Attributes",
                "Name:="		, _name,
                "Flags:="		, "",
                "Color:="		, "(143 175 143)",
                "Transparency:="	, 0,
                "PartCoordinateSystem:=", "Global",
                "UDMId:="		, "",
                "MaterialValue:="	, "\"pec\"",
                "SurfaceMaterialValue:=", "\"\"",
                "SolveInside:="		, False,
                "IsMaterialEditable:="	, True,
                "UseMaterialAppearance:=", False
            ])



    def assign_sheet_pec(self, _structure_name, _bd_name="PerfE1"):
        mod = self.oDesign.GetModule("BoundarySetup")
        mod.AssignPerfectE(
            [
                "NAME:" + _bd_name,
                "Objects:=", [_structure_name],
                "InfGroundPlane:=", False
            ])

    def assign_mater_slave_boundary_condition(self, _obj ):
        _b_xyz = self.oEditor.GetModelBoundingBox()
        _bounding_xyz =numpy.zeros(6)
        i = 0
        for _string in _b_xyz:
            _bounding_xyz[i] = float(_string)
            i += 1


        self.oModule = self.oDesign.GetModule("BoundarySetup")

        _surf_ind = numpy.ones(3)
        _surf_ind[0] = _bounding_xyz[0]
        _surf_ind[1] = 0.4 * _bounding_xyz[1] + 0.6 * _bounding_xyz[4]
        _surf_ind[2] = 0.4 * _bounding_xyz[2] + 0.6 * _bounding_xyz[5]

        _master_ID_x = self.oEditor.GetFaceByPosition(
            [
                "NAME:FaceParameters",
                "BodyName:=", _obj,
                "XPosition:=", str(_surf_ind[0]) + "mm",
                "YPosition:=", str(_surf_ind[1]) + "mm",
                "ZPosition:=", str(_surf_ind[2]) + "mm"
            ])


        self.oModule.AssignMaster(
            [
                "NAME:Master_x",
                "Faces:="	, [_master_ID_x],
                [
                    "NAME:CoordSysVector",
                    "Origin:="	, [str(_bounding_xyz[0])+"mm",
                                     str(_bounding_xyz[1]) + "mm",
                                     str(_bounding_xyz[2]) +"mm"],
                    "UPos:="	, [str(_bounding_xyz[0])+"mm",
                                   str(_bounding_xyz[4]) + "mm",
                                   str(_bounding_xyz[2]) +"mm"]
                ],
                "ReverseV:="		, False
            ])


        _surf_ind[0] = _bounding_xyz[3]
        _surf_ind[1] = 0.4 * _bounding_xyz[1] + 0.6 * _bounding_xyz[4]
        _surf_ind[2] = 0.4 * _bounding_xyz[2] + 0.6 * _bounding_xyz[5]

        _slave_ID_x = self.oEditor.GetFaceByPosition(
            [
                "NAME:FaceParameters",
                "BodyName:=", _obj,
                "XPosition:=", str(_surf_ind[0]) + "mm",
                "YPosition:=", str(_surf_ind[1]) + "mm",
                "ZPosition:=", str(_surf_ind[2]) + "mm"
            ])

        self.oModule.AssignSlave(
            [
                "NAME:Slave_x",
                "Faces:=", [_slave_ID_x],
                [
                    "NAME:CoordSysVector",
                    "Origin:="	, [str(_bounding_xyz[3])+"mm",
                                     str(_bounding_xyz[1]) + "mm",
                                     str(_bounding_xyz[2]) +"mm"],
                    "UPos:="	, [str(_bounding_xyz[3])+"mm",
                                   str(_bounding_xyz[4]) + "mm",
                                   str(_bounding_xyz[2]) +"mm"]
                ],
                "ReverseV:="	, True,
                "Master:="	, "Master_x",
                "UseScanAngles:="	, True,
                "Phi:="			, "0deg",
                "Theta:="		, "0deg"
            ])

        _surf_ind[0] = 0.4 * _bounding_xyz[0] + 0.6 * _bounding_xyz[3]
        _surf_ind[1] = _bounding_xyz[1]
        _surf_ind[2] = 0.4 * _bounding_xyz[2] + 0.6 * _bounding_xyz[5]

        _master_ID_y = self.oEditor.GetFaceByPosition(
            [
                "NAME:FaceParameters",
                "BodyName:=", _obj,
                "XPosition:=", str(_surf_ind[0]) + "mm",
                "YPosition:=", str(_surf_ind[1]) + "mm",
                "ZPosition:=", str(_surf_ind[2]) + "mm"
            ])

        self.oModule.AssignMaster(
            [
                "NAME:Master_y",
                "Faces:=", [_master_ID_y],
                [
                    "NAME:CoordSysVector",
                    "Origin:="	, [str(_bounding_xyz[0])+"mm",
                                     str(_bounding_xyz[1]) + "mm",
                                     str(_bounding_xyz[2]) +"mm"],
                    "UPos:="	, [str(_bounding_xyz[3])+"mm",
                                   str(_bounding_xyz[1]) + "mm",
                                   str(_bounding_xyz[2]) +"mm"]
                ],
                "ReverseV:="	, True
            ])

        _surf_ind[0] = 0.4 * _bounding_xyz[0] + 0.6 * _bounding_xyz[3]
        _surf_ind[1] = _bounding_xyz[4]
        _surf_ind[2] = 0.4 * _bounding_xyz[2] + 0.6 * _bounding_xyz[5]

        _slave_ID_y = self.oEditor.GetFaceByPosition(
            [
                "NAME:FaceParameters",
                "BodyName:=", _obj,
                "XPosition:=", str(_surf_ind[0]) + "mm",
                "YPosition:=", str(_surf_ind[1]) + "mm",
                "ZPosition:=", str(_surf_ind[2]) + "mm"
            ])

        self.oModule.AssignSlave(
            [
                "NAME:Slave_y",
                "Faces:=", [_slave_ID_y],
                [
                    "NAME:CoordSysVector",
                    "Origin:="	, [str(_bounding_xyz[0])+"mm",
                                     str(_bounding_xyz[4]) + "mm",
                                     str(_bounding_xyz[2]) +"mm"],
                    "UPos:="	, [str(_bounding_xyz[3])+"mm",
                                   str(_bounding_xyz[4]) + "mm",
                                   str(_bounding_xyz[2]) +"mm"]
                ],
                "ReverseV:=", False,
                "Master:=", "Master_y",
                "UseScanAngles:=", True,
                "Phi:="		, "0deg",
                "Theta:="		, "0deg"
            ])

    def assign_floque_port(self, _obj, _solution_freq ):

        _b_xyz = self.oEditor.GetModelBoundingBox()
        _bounding_xyz = numpy.zeros(6)
        i = 0
        for _string in _b_xyz:
            _bounding_xyz[i] = float(_string)
            i += 1

        self.oModule = self.oDesign.GetModule("BoundarySetup")

        _surf_ind = numpy.ones(3)
        _surf_ind[0] = 0.0
        _surf_ind[1] = 0.0
        _surf_ind[2] = _bounding_xyz[2]

        _port_ID_z = self.oEditor.GetFaceByPosition(
            [
                "NAME:FaceParameters",
                "BodyName:=", _obj,
                "XPosition:=", str(_surf_ind[0]) + "mm",
                "YPosition:=", str(_surf_ind[1]) + "mm",
                "ZPosition:=", str(_surf_ind[2]) + "mm"
            ])
        self.oModule.AssignFloquetPort(
            [
                "NAME:FloquetPort1",
                "Faces:="		, [_port_ID_z],
                "NumModes:="		, 2,
                "RenormalizeAllTerminals:=", True,
                "DoDeembed:="		, True,
		        "DeembedDist:="		, str(abs(_bounding_xyz[2]))+"mm",
                [
                    "NAME:Modes",
                    [
                        "NAME:Mode1",
                        "ModeNum:="		, 1,
                        "UseIntLine:="		, False,
                        "CharImp:="		, "Zpi"
                    ],
                    [
                        "NAME:Mode2",
                        "ModeNum:="		, 2,
                        "UseIntLine:="		, False,
                        "CharImp:="		, "Zpi"
                    ]
                ],
                "ShowReporterFilter:="	, False,
                "ReporterFilter:="	, [False,False],
                "UseScanAngles:="	, True,
                "Phi:="			, "0deg",
                "Theta:="		, "0deg",
                [
                    "NAME:LatticeAVector",
                    "Start:="		, [str(_bounding_xyz[0])+"mm",
                                        str(_bounding_xyz[1])+"mm",
                                        str(_bounding_xyz[2]) + "mm"],
                    "End:="			, [str(_bounding_xyz[3])+"mm",
                                          str(_bounding_xyz[1])+"mm",
                                          str(_bounding_xyz[2]) + "mm"],
                ],
                [
                    "NAME:LatticeBVector",
                    "Start:="		, [str(_bounding_xyz[0])+"mm",
                                        str(_bounding_xyz[1])+"mm",
                                        str(_bounding_xyz[2]) + "mm"],
                    "End:="			, [str(_bounding_xyz[0])+"mm",
                                          str(_bounding_xyz[4])+"mm",
                                          str(_bounding_xyz[2]) + "mm"],
                ],
                [
                    "NAME:ModesCalculator",
                    "Frequency:="		, str(_solution_freq) + "GHz",
                    "FrequencyChanged:="	, True,
                    "PhiStart:="		, "0deg",
                    "PhiStop:="		, "0deg",
                    "PhiStep:="		, "0deg",
                    "ThetaStart:="		, "0deg",
                    "ThetaStop:="		, "0deg",
                    "ThetaStep:="		, "0deg"
                ],
                [
                    "NAME:ModesList",
                    [
                        "NAME:Mode",
                        "ModeNumber:="		, 1,
                        "IndexM:="		, 0,
                        "IndexN:="		, 0,
                        "KC2:="			, 0,
                        "PropagationState:="	, "Propagating",
                        "Attenuation:="		, 0,
                        "PolarizationState:="	, "TE",
                        "AffectsRefinement:="	, True
                    ],
                    [
                        "NAME:Mode",
                        "ModeNumber:="		, 2,
                        "IndexM:="		, 0,
                        "IndexN:="		, 0,
                        "KC2:="			, 0,
                        "PropagationState:="	, "Propagating",
                        "Attenuation:="		, 0,
                        "PolarizationState:="	, "TM",
                        "AffectsRefinement:="	, True
                    ]
                ]
            ])


        _surf_ind[2] = _bounding_xyz[5]

        _port_ID_z = self.oEditor.GetFaceByPosition(
            [
                "NAME:FaceParameters",
                "BodyName:=", _obj,
                "XPosition:=", str(_surf_ind[0]) + "mm",
                "YPosition:=", str(_surf_ind[1]) + "mm",
                "ZPosition:=", str(_surf_ind[2]) + "mm"
            ])
        self.oModule.AssignFloquetPort(
            [
                "NAME:FloquetPort2",
                "Faces:="		, [_port_ID_z],
                "NumModes:="		, 2,
                "RenormalizeAllTerminals:=", True,
                "DoDeembed:="		, True,
		        "DeembedDist:="		, str(abs(_bounding_xyz[5]))+"mm",
                [
                    "NAME:Modes",
                    [
                        "NAME:Mode1",
                        "ModeNum:="		, 1,
                        "UseIntLine:="		, False,
                        "CharImp:="		, "Zpi"
                    ],
                    [
                        "NAME:Mode2",
                        "ModeNum:="		, 2,
                        "UseIntLine:="		, False,
                        "CharImp:="		, "Zpi"
                    ]
                ],
                "ShowReporterFilter:="	, False,
                "ReporterFilter:="	, [False,False],
                "UseScanAngles:="	, True,
                "Phi:="			, "0deg",
                "Theta:="		, "0deg",
                [
                    "NAME:LatticeAVector",
                    "Start:="	, [str(_bounding_xyz[0] ) +"mm",
                                        str(_bounding_xyz[1] ) +"mm",
                                        str(_bounding_xyz[5]) + "mm"],
                    "End:="			, [str(_bounding_xyz[3] ) +"mm",
                                          str(_bounding_xyz[1] ) +"mm",
                                          str(_bounding_xyz[5]) + "mm"],
                ],
                [
                    "NAME:LatticeBVector",
                    "Start:="		, [str(_bounding_xyz[0] ) +"mm",
                                        str(_bounding_xyz[1] ) +"mm",
                                        str(_bounding_xyz[5]) + "mm"],
                    "End:="			, [str(_bounding_xyz[0] ) +"mm",
                                          str(_bounding_xyz[4] ) +"mm",
                                          str(_bounding_xyz[5]) + "mm"],
                ],
                [
                    "NAME:ModesCalculator",
                    "Frequency:="		, str(_solution_freq) + "GHz",
                    "FrequencyChanged:="	, True,
                    "PhiStart:="		, "0deg",
                    "PhiStop:="		, "0deg",
                    "PhiStep:="		, "0deg",
                    "ThetaStart:="		, "0deg",
                    "ThetaStop:="		, "0deg",
                    "ThetaStep:="		, "0deg"
                ],
                [
                    "NAME:ModesList",
                    [
                        "NAME:Mode",
                        "ModeNumber:="		, 1,
                        "IndexM:="		, 0,
                        "IndexN:="		, 0,
                        "KC2:="			, 0,
                        "PropagationState:="	, "Propagating",
                        "Attenuation:="		, 0,
                        "PolarizationState:="	, "TE",
                        "AffectsRefinement:="	, True
                    ],
                    [
                        "NAME:Mode",
                        "ModeNumber:="		, 2,
                        "IndexM:="		, 0,
                        "IndexN:="		, 0,
                        "KC2:="			, 0,
                        "PropagationState:="	, "Propagating",
                        "Attenuation:="		, 0,
                        "PolarizationState:="	, "TM",
                        "AffectsRefinement:="	, True
                    ]
                ]
            ])

    def gen_meta_with_surf(self, _mat_surf: Meta_Generator.Meta_Surf):
        n_pix = 0
        _n = _mat_surf.n
        pix_l = 1.00 * _mat_surf.pix_l
        z_bot = str(-_mat_surf.t * 0.5) + 'mm'
        z_up = str(_mat_surf.t ) + 'mm'
        a = _mat_surf.a

        for i in range(2 * _n):
            for j in range(2 * _n):
                if a[i, j] == 0:


                    ind_x = str((j - _n) * pix_l) + "mm"
                    ind_y = str((i - _n) * pix_l) + "mm"

                    if( i == 2*_n or j == 2*_n):
                        _ll = pix_l
                    else:
                        _ll = pix_l

                    n_pix = n_pix + 1
                    pix_name = "pix_" + str(n_pix)
                    self.create_box(ind_x, ind_y, z_bot, str(_ll) + "mm", str(_ll) + "mm", z_up,
                                 pix_name, 'pec')

                    if( n_pix != 1 ):
                        self.unite( "pix_1", pix_name )

        for i in range(1,2 * _n - 1):
            for j in range(1, 2 * _n - 1):
                if a[i, j] == 0.5:

                    ind_x = (j - _n) * pix_l
                    ind_y = (i - _n) * pix_l
                    ind_z = -_mat_surf.t * 0.5
                    _t = _mat_surf.t


                    if (a[i-1,j] == 0 and a[i,j+1] == 0):
                        n_pix = n_pix + 1
                        pix_name = "pix_" + str(n_pix)
                        self.create_box_trian(ind_x, ind_y, ind_z, pix_l, pix_l, _t, 1, pix_name, 'pec')
                        self.unite("pix_1", pix_name)
                    if (a[i,j+1] == 0 and a[i+1,j] == 0):
                        n_pix = n_pix + 1
                        pix_name = "pix_" + str(n_pix)
                        self.create_box_trian(ind_x, ind_y, ind_z, pix_l, pix_l, _t, 2, pix_name,  'pec')
                        self.unite("pix_1", pix_name)
                    if (a[i+1,j] == 0 and a[i,j-1] == 0):
                        n_pix = n_pix + 1
                        pix_name = "pix_" + str(n_pix)
                        self.create_box_trian(ind_x, ind_y, ind_z, pix_l, pix_l, _t, 3, pix_name,  'pec')
                        self.unite("pix_1", pix_name)
                    if (a[i,j-1] == 0 and a[i-1,j] == 0):
                        n_pix = n_pix + 1
                        pix_name = "pix_" + str(n_pix)
                        self.create_box_trian(ind_x, ind_y, ind_z, pix_l, pix_l, _t, 4, pix_name,  'pec')
                        self.unite("pix_1", pix_name)






    def gen_meta_with_surf_025(self, _mat_surf: Meta_Generator.Meta_Surf):
        n_pix = 0
        _n = _mat_surf.n
        pix_l = 1.00 * _mat_surf.pix_l
        z_bot = str(-_mat_surf.t * 0.5) + 'mm'
        z_up = str(_mat_surf.t ) + 'mm'
        a = _mat_surf.a

        for i in range( _n):
            for j in range( _n):
                if a[i, j] == 0:


                    ind_x = str((j - _n) * pix_l) + "mm"
                    ind_y = str((i - _n) * pix_l) + "mm"

                    if( i == 2*_n or j == 2*_n):
                        _ll = pix_l
                    else:
                        _ll = pix_l

                    n_pix = n_pix + 1
                    pix_name = "pix_" + str(n_pix)
                    self.create_box(ind_x, ind_y, z_bot, str(_ll) + "mm", str(_ll) + "mm", z_up,
                                 pix_name, 'pec')

                    if( n_pix != 1 ):
                        self.unite( "pix_1", pix_name )

        for i in range(0, _n ):
            for j in range(0,  _n ):
                if a[i, j] == 0.5:

                    ind_x = (j - _n) * pix_l
                    ind_y = (i - _n) * pix_l
                    ind_z = -_mat_surf.t * 0.5
                    _t = _mat_surf.t

                    if( i != 0 and j != _n):
                        if (a[i-1,j] == 0 and a[i,j+1] == 0):
                            n_pix = n_pix + 1
                            pix_name = "pix_" + str(n_pix)
                            self.create_box_trian(ind_x, ind_y, ind_z, pix_l, pix_l, _t, 1, pix_name, 'pec')
                            self.unite("pix_1", pix_name)
                    if (i != _n and j != _n):
                        if (a[i,j+1] == 0 and a[i+1,j] == 0):
                            n_pix = n_pix + 1
                            pix_name = "pix_" + str(n_pix)
                            self.create_box_trian(ind_x, ind_y, ind_z, pix_l, pix_l, _t, 2, pix_name,  'pec')
                            self.unite("pix_1", pix_name)
                    if (i != _n and j != 0):
                        if (a[i+1,j] == 0 and a[i,j-1] == 0):
                            n_pix = n_pix + 1
                            pix_name = "pix_" + str(n_pix)
                            self.create_box_trian(ind_x, ind_y, ind_z, pix_l, pix_l, _t, 3, pix_name,  'pec')
                            self.unite("pix_1", pix_name)
                    if (i != 0 and j != 0):
                        if (a[i,j-1] == 0 and a[i-1,j] == 0):
                            n_pix = n_pix + 1
                            pix_name = "pix_" + str(n_pix)
                            self.create_box_trian(ind_x, ind_y, ind_z, pix_l, pix_l, _t, 4, pix_name,  'pec')
                            self.unite("pix_1", pix_name)

        self.duplicate_mirror("pix_1", "yz")
        self.unite("pix_1", "pix_1_1")

        self.duplicate_mirror("pix_1", "zx")
        self.unite("pix_1", "pix_1_2")

if __name__ == '__HFSS_Script__':


    h = HFSS( )


    h.new_design( "test1")
    h.set_variable('_freq', 10.00)
    h.set_variable('_thickness', 0.1, 'mm')
    h.set_variable('_pix_l', 1,'mm')

    h.create_box('-2*_pix_l*0.5', '-2*_pix_l*0.5', '-_thickness*0.5',
                 '2*_pix_l', '2*_pix_l', '_thickness', 'Pix_a', 'pec')

    h.create_box('_pix_l*0.5', '_pix_l*0.5', '-_thickness*0.5',
                 '2*_pix_l', '2*_pix_l', '_thickness', 'Pix_b', 'pec')

    h.unite('Pix_a', 'Pix_b')

    h.create_box('-_pix_l*5', '-_pix_l*5', '-_pix_l*10',
                 '_pix_l*10', '_pix_l*10', '_pix_l*20', 'Boundary')

    h.assign_mater_slave_boundary_condition('Boundary')
    h.assign_floque_port('Boundary', 10.0)

    h.insert_analysis_setup("s1", 10.0)
    h.insert_frequency_swap("s1",7.50, 12.5, 100)
    h.run("s1")
    h.save_prj()
    # h.set_variable('wg_a', 22.86)
    # h.set_variable('wg_b', 10.16)
    #
    # h.create_centered_rectangle('wg_a', 'wg_b', 0, 'wg_in')
    #
    # h.new_design("test2")
    # h.set_variable('wg_a', 22.86)
    # h.set_variable('wg_b', 10.16)
    #
    # h.create_centered_rectangle('wg_b', 'wg_a', 0, 'wg_in')