"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var disposable_1 = require("@phosphor/disposable");
var manager_1 = require("./manager");
var renderer_1 = require("./renderer");
var NBWidgetExtension = /** @class */ (function () {
    function NBWidgetExtension() {
    }
    NBWidgetExtension.prototype.createNew = function (nb, context) {
        var manager = new manager_1.ContextManager(context);
        nb.rendermime.addFactory({
            safe: false,
            mimeTypes: [renderer_1.BOKEHJS_LOAD_MIME_TYPE],
            createRenderer: function (options) { return new renderer_1.BokehJSLoad(options); }
        }, 0);
        // the rank has to be -1, so that the priority is higher than the
        // default javascript mime extension (rank=0)
        nb.rendermime.addFactory({
            safe: false,
            mimeTypes: [renderer_1.BOKEHJS_EXEC_MIME_TYPE],
            createRenderer: function (options) { return new renderer_1.BokehJSExec(options, manager); }
        }, -1);
        return new disposable_1.DisposableDelegate(function () {
            if (nb.rendermime) {
                nb.rendermime.removeMimeType(renderer_1.BOKEHJS_EXEC_MIME_TYPE);
            }
            manager.dispose();
        });
    };
    return NBWidgetExtension;
}());
exports.NBWidgetExtension = NBWidgetExtension;
exports.extension = {
    id: 'jupyterlab_bokeh',
    autoStart: true,
    activate: function (app) {
        // this adds the Bokeh widget extension onto Notebooks specifically
        app.docRegistry.addWidgetExtension('Notebook', new NBWidgetExtension());
    }
};
