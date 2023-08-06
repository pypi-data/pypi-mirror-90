(self["webpackChunkjupyterlab_ngl"] = self["webpackChunkjupyterlab_ngl"] || []).push([["lib_index_js-webpack_sharing_consume_default_react-dom"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => __WEBPACK_DEFAULT_EXPORT__
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./widget */ "./lib/widget.js");




/**
 * The command IDs used by the react-widget plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.create = 'create-react-widget';
})(CommandIDs || (CommandIDs = {}));
/**
 * Initialization data for the react-widget extension.
 */
const extension = {
    id: 'react-widget',
    autoStart: true,
    optional: [_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_1__.ILauncher],
    activate: (app, launcher) => {
        const { commands } = app;
        const command = CommandIDs.create;
        commands.addCommand(command, {
            caption: 'Create a new React Widget',
            label: 'NGL Visualizer',
            icon: args => (args['isPalette'] ? null : _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.reactIcon),
            execute: () => {
                const content = new _widget__WEBPACK_IMPORTED_MODULE_3__.CounterWidget();
                const widget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.MainAreaWidget({ content });
                widget.title.label = 'NGL Visualizer';
                app.shell.add(widget, 'main');
            }
        });
        if (launcher) {
            launcher.add({
                command
            });
        }
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extension);


/***/ }),

/***/ "./lib/sliders.js":
/*!************************!*\
  !*** ./lib/sliders.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => /* binding */ VerticalSlider
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _material_ui_core_styles__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @material-ui/core/styles */ "./node_modules/@material-ui/core/esm/styles/makeStyles.js");
/* harmony import */ var _material_ui_core_Slider__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @material-ui/core/Slider */ "./node_modules/@material-ui/core/esm/Slider/Slider.js");
/* harmony import */ var _material_ui_core_styles__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @material-ui/core/styles */ "./node_modules/@material-ui/core/esm/styles/createMuiTheme.js");
/* harmony import */ var _material_ui_core_styles__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @material-ui/core/styles */ "./node_modules/@material-ui/styles/esm/ThemeProvider/ThemeProvider.js");
/* harmony import */ var _material_ui_core_CssBaseline__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @material-ui/core/CssBaseline */ "./node_modules/@material-ui/core/esm/CssBaseline/CssBaseline.js");
/* harmony import */ var _material_ui_core_Box__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @material-ui/core/Box */ "./node_modules/@material-ui/core/esm/Box/Box.js");
/* harmony import */ var _material_ui_core_Grid__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @material-ui/core/Grid */ "./node_modules/@material-ui/core/esm/Grid/Grid.js");







function VerticalSlider(Props) {
    const useStyles = (0,_material_ui_core_styles__WEBPACK_IMPORTED_MODULE_1__.default)({
        root: {
            flexGrow: 1,
            marginTop: '40px',
            width: '700px',
            marginLeft: '60px'
        }
    });
    function valuetext(value) {
        return `${value}°C`;
    }
    const marks2 = [
        {
            value: -0.04,
            label: '-0.04'
        },
        {
            value: -0.02,
            label: '-0.02'
        },
        {
            value: 0,
            label: '0'
        },
        {
            value: 0.02,
            label: '0.02'
        },
        {
            value: 0.04,
            label: '0.04'
        }
    ];
    const marks1 = [
        {
            value: 0,
            label: '0%'
        },
        {
            value: 20,
            label: '20%'
        },
        {
            value: 40,
            label: '40%'
        },
        {
            value: 60,
            label: '60%'
        },
        {
            value: 80,
            label: '80%'
        },
        {
            value: 100,
            label: '100%'
        }
    ];
    const classes = useStyles();
    const darkTheme = (0,_material_ui_core_styles__WEBPACK_IMPORTED_MODULE_2__.default)({
        palette: {
            type: 'dark'
        }
    });
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_styles__WEBPACK_IMPORTED_MODULE_3__.default, { theme: darkTheme },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_CssBaseline__WEBPACK_IMPORTED_MODULE_4__.default, null),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: classes.root },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_Grid__WEBPACK_IMPORTED_MODULE_5__.default, { container: true, spacing: 3, justify: "center" },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_Grid__WEBPACK_IMPORTED_MODULE_5__.default, { item: true, sm: 10 },
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_Box__WEBPACK_IMPORTED_MODULE_6__.default, { id: Props.uuid, style: {
                                width: '600px',
                                height: '400px',
                                backgroundColor: 'black'
                            } })),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_Grid__WEBPACK_IMPORTED_MODULE_5__.default, { item: true, sm: 1 },
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_Slider__WEBPACK_IMPORTED_MODULE_7__.default, { orientation: "vertical", getAriaValueText: valuetext, valueLabelDisplay: "auto", defaultValue: 30, "aria-labelledby": "vertical-slider", min: 0, max: 100, marks: marks1, onChange: Props.changeHandler1, color: 'primary' })),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_Grid__WEBPACK_IMPORTED_MODULE_5__.default, { item: true, sm: 1 },
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_Slider__WEBPACK_IMPORTED_MODULE_7__.default, { orientation: "vertical", defaultValue: [0.01, -0.01], "aria-labelledby": "vertical-slider", getAriaValueText: valuetext, valueLabelDisplay: "on", marks: marks2, min: -0.04, max: 0.04, step: 0.001, onChange: Props.changeHandler2, color: 'secondary' })))))));
}


/***/ }),

/***/ "./lib/switches.js":
/*!*************************!*\
  !*** ./lib/switches.js ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => /* binding */ SwitchLabels
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _material_ui_core_FormGroup__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @material-ui/core/FormGroup */ "./node_modules/@material-ui/core/esm/FormGroup/FormGroup.js");
/* harmony import */ var _material_ui_core_FormControlLabel__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @material-ui/core/FormControlLabel */ "./node_modules/@material-ui/core/esm/FormControlLabel/FormControlLabel.js");
/* harmony import */ var _material_ui_core_Switch__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @material-ui/core/Switch */ "./node_modules/@material-ui/core/esm/Switch/Switch.js");
/* harmony import */ var _material_ui_core_styles__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @material-ui/core/styles */ "./node_modules/@material-ui/core/esm/styles/makeStyles.js");





function SwitchLabels(Props) {
    const useStyles = (0,_material_ui_core_styles__WEBPACK_IMPORTED_MODULE_1__.default)(theme => ({
        container: {
            display: 'flex',
            flexWrap: 'wrap',
            position: 'absolute',
            top: 0,
            left: 0,
            height: '100%',
            width: '100%',
            alignItems: 'center'
        },
        textField: {
            marginLeft: theme.spacing(1),
            marginRight: theme.spacing(1),
            width: 200
        },
        formGroup: {
            alignItems: 'center',
            marginLeft: '100px'
        }
    }));
    const classes = useStyles();
    const [state, setState] = react__WEBPACK_IMPORTED_MODULE_0___default().useState({
        checkedA: false,
        checkedB: true,
        checkedC: true
    });
    const handleChange1 = (event) => {
        setState({ ...state, [event.target.name]: event.target.checked });
        Props.clickHandler1();
    };
    const handleChange2 = (event) => {
        setState({ ...state, [event.target.name]: event.target.checked });
        Props.clickHandler2();
    };
    const handleChange3 = (event) => {
        setState({ ...state, [event.target.name]: event.target.checked });
        Props.clickHandler3();
    };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null,
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_FormGroup__WEBPACK_IMPORTED_MODULE_2__.default, { className: classes.formGroup, row: true },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_FormControlLabel__WEBPACK_IMPORTED_MODULE_3__.default, { control: react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_Switch__WEBPACK_IMPORTED_MODULE_4__.default, { checked: state.checkedA, onChange: handleChange1, name: "checkedA" }), label: "Toggle Spin" }),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_FormControlLabel__WEBPACK_IMPORTED_MODULE_3__.default, { control: react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_Switch__WEBPACK_IMPORTED_MODULE_4__.default, { checked: state.checkedB, onChange: handleChange2, name: "checkedB", color: "primary" }), label: "Alpha" }),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_FormControlLabel__WEBPACK_IMPORTED_MODULE_3__.default, { control: react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_Switch__WEBPACK_IMPORTED_MODULE_4__.default, { checked: state.checkedC, onChange: handleChange3, name: "checkedC", color: "secondary" }), label: "Beta" }))));
}


/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CounterWidget": () => /* binding */ CounterWidget
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var ngl__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ngl */ "webpack/sharing/consume/default/ngl/ngl");
/* harmony import */ var ngl__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(ngl__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _material_ui_core_Button__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @material-ui/core/Button */ "./node_modules/@material-ui/core/esm/Button/Button.js");
/* harmony import */ var underscore__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! underscore */ "webpack/sharing/consume/default/underscore/underscore");
/* harmony import */ var underscore__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(underscore__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _sliders__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./sliders */ "./lib/sliders.js");
/* harmony import */ var _switches__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./switches */ "./lib/switches.js");







/**
 * A Counter Lumino Widget that wraps a CounterComponent.
 */
class CounterWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ReactWidget {
    constructor() {
        super();
        this.addClass('jp-ReactWidget');
        this.uuid = underscore__WEBPACK_IMPORTED_MODULE_3__.uniqueId('ngl_');
        window.requestAnimationFrame(() => {
            this.visualizer();
        });
    }
    visualizer() {
        ngl__WEBPACK_IMPORTED_MODULE_2__.DatasourceRegistry.add('data', new ngl__WEBPACK_IMPORTED_MODULE_2__.StaticDatasource('//cdn.rawgit.com/arose/ngl/v2.0.0-dev.32/data/'));
        const stage = new ngl__WEBPACK_IMPORTED_MODULE_2__.Stage(this.uuid, { backgroundColor: 'black' });
        window.addEventListener('resize', event => {
            stage.handleResize();
        }, false);
        stage.viewer.container.addEventListener('dblclick', () => {
            stage.toggleFullscreen();
        });
        stage
            .loadFile('data://benzene.sdf', { name: 'structure1' })
            .then((o) => {
            const atomTriple = [[0, 1, 2]];
            o.addRepresentation('ball+stick');
            o.addRepresentation('label', {
                labelType: 'atomindex',
                color: 'white'
            });
            o.addRepresentation('angle', {
                atomTriple: atomTriple,
                labelSize: 1.0,
                labelColor: 'yellow',
                sdf: false
            });
            o.autoView();
        });
        stage
            .loadFile('data://benzene-homo.cube', { name: 'surface_1' })
            .then((o) => {
            o.addRepresentation('surface', {
                visible: true,
                isolevelType: 'value',
                isolevel: 0.01,
                color: 'blue',
                opacity: 0.7,
                opaqueBack: false
            });
            o.signals.visibilityChanged.add((value) => {
                console.log('Dou Du****:' + value);
            });
            o.autoView();
        });
        stage
            .loadFile('data://benzene-homo.cube', { name: 'surface_2' })
            .then((o) => {
            o.addRepresentation('surface', {
                visible: true,
                isolevelType: 'value',
                isolevel: -0.01,
                color: 'red',
                opacity: 0.7,
                opaqueBack: false
            });
            o.autoView();
        });
        this.stage = stage;
    }
    updateIsosurface(e) {
        this.stage
            .getRepresentationsByName('surface')
            .setParameters({ opacity: e });
        this.stage.getComponentsByName('surface_1').list[0].setVisibility(true);
        this.stage.getComponentsByName('surface_2').list[0].setVisibility(true);
    }
    updateIsolevel(e, filename) {
        this.stage
            .getComponentsByName(filename)
            .list[0].eachRepresentation((reprElem) => {
            reprElem.setParameters({ isolevel: e });
        });
    }
    toggleVisibility(filename) {
        const a = this.stage.getComponentsByName(filename).list[0];
        a.setVisibility(!a.visible);
    }
    setVisibility(filename, val) {
        const a = this.stage.getComponentsByName(filename).list[0];
        a.setVisibility(val);
    }
    toggleSpin() {
        this.stage.toggleSpin();
    }
    render() {
        const func1 = () => this.stage.toggleSpin();
        const func2 = () => this.toggleVisibility('surface_1');
        const func3 = () => this.toggleVisibility('surface_2');
        return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", null,
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { style: { width: '30%' } },
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_sliders__WEBPACK_IMPORTED_MODULE_4__.default, { uuid: this.uuid, changeHandler1: (event, val) => {
                        const value = val / 100.0;
                        this.updateIsosurface(value);
                    }, changeHandler2: (event, val) => {
                        const value = val;
                        this.updateIsolevel(value[0], 'surface_1');
                        this.updateIsolevel(value[1], 'surface_2');
                    } })),
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { style: { marginLeft: '200px', marginTop: '10px' } },
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_material_ui_core_Button__WEBPACK_IMPORTED_MODULE_5__.default, { color: "primary", variant: "contained", onClick: () => {
                        this.toggleVisibility('surface_1');
                        this.toggleVisibility('surface_2');
                    } }, "Toggle surface"),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_material_ui_core_Button__WEBPACK_IMPORTED_MODULE_5__.default, { style: { marginLeft: '30px' }, color: "secondary", variant: "contained", onClick: () => {
                        this.toggleVisibility('structure1');
                    } }, "Toggle structure")),
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_switches__WEBPACK_IMPORTED_MODULE_6__.default, { clickHandler1: func1, clickHandler2: func2, clickHandler3: func3 })));
    }
}


/***/ })

}]);
//# sourceMappingURL=lib_index_js-webpack_sharing_consume_default_react-dom.485435b50d756bfcfec9.js.map