"use strict";
var __extends = (this && this.__extends) || (function () {
    var extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
var widgets_1 = require("@phosphor/widgets");
/**
 * The MIME types for BokehJS.
 */
var HTML_MIME_TYPE = 'text/html';
var JS_MIME_TYPE = 'application/javascript';
exports.BOKEHJS_LOAD_MIME_TYPE = 'application/vnd.bokehjs_load.v0+json';
exports.BOKEHJS_EXEC_MIME_TYPE = 'application/vnd.bokehjs_exec.v0+json';
/**
 * Load BokehJS and CSS into the DOM
 */
var BokehJSLoad = /** @class */ (function (_super) {
    __extends(BokehJSLoad, _super);
    function BokehJSLoad(options) {
        var _this = _super.call(this) || this;
        _this._load_mimetype = exports.BOKEHJS_LOAD_MIME_TYPE;
        _this._script_element = document.createElement("script");
        return _this;
    }
    BokehJSLoad.prototype.renderModel = function (model) {
        var data = model.data[this._load_mimetype];
        this._script_element.textContent = data;
        this.node.appendChild(this._script_element);
        return Promise.resolve();
    };
    return BokehJSLoad;
}(widgets_1.Widget));
exports.BokehJSLoad = BokehJSLoad;
/**
 * Exec BokehJS in window
 */
var BokehJSExec = /** @class */ (function (_super) {
    __extends(BokehJSExec, _super);
    function BokehJSExec(options, manager) {
        var _this = _super.call(this) || this;
        // for classic nb compat reasons, the payload in contained in these mime messages
        _this._html_mimetype = HTML_MIME_TYPE;
        _this._js_mimetype = JS_MIME_TYPE;
        // the metadata is stored here
        _this._exec_mimetype = exports.BOKEHJS_EXEC_MIME_TYPE;
        _this._script_element = document.createElement("script");
        _this._manager = manager;
        return _this;
    }
    Object.defineProperty(BokehJSExec.prototype, "isDisposed", {
        get: function () {
            return this._manager === null;
        },
        enumerable: true,
        configurable: true
    });
    BokehJSExec.prototype.renderModel = function (model) {
        var _this = this;
        var metadata = model.metadata[this._exec_mimetype];
        if (metadata.id !== undefined) {
            // I'm a static document
            var data = model.data[this._js_mimetype];
            this._script_element.textContent = data;
            if (window.Bokeh !== undefined && window.Bokeh.embed.kernels !== undefined) {
                this._document_id = metadata.id;
                var registerClosure = function (targetName, callback) {
                    _this._manager.context.session.kernel.registerCommTarget(targetName, callback);
                };
                var kernel_proxy = {
                    registerCommTarget: registerClosure
                };
                window.Bokeh.embed.kernels[this._document_id] = kernel_proxy;
                this._manager.context.session.statusChanged.connect(function (session, status) {
                    if (status == "restarting" || status === "dead") {
                        delete window.Bokeh.embed.kernels[_this._document_id];
                    }
                }, this);
            }
        }
        else if (metadata.server_id !== undefined) {
            // I'm a server document
            this._server_id = metadata.server_id;
            var data = model.data[this._html_mimetype];
            var d = document.createElement('div');
            d.innerHTML = data;
            var script_attrs = d.children[0].attributes;
            for (var i in script_attrs) {
                this._script_element.setAttribute(script_attrs[i].name, script_attrs[i].value);
            }
        }
        this.node.appendChild(this._script_element);
        return Promise.resolve();
    };
    BokehJSExec.prototype.dispose = function () {
        if (this.isDisposed) {
            return;
        }
        if (this._server_id) {
            var content = {
                code: "import bokeh.io.notebook as ion; ion.destroy_server('" + this._server_id + "')"
            };
            this._manager.context.session.kernel.requestExecute(content, true);
            this._server_id = null;
        }
        else if (this._document_id) {
            if (window.Bokeh.embed.kernels !== undefined) {
                delete window.Bokeh.embed.kernels[this._document_id];
            }
            this._document_id = null;
        }
        this._manager = null;
    };
    return BokehJSExec;
}(widgets_1.Widget));
exports.BokehJSExec = BokehJSExec;
