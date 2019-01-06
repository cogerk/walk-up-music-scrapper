"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
/**
 * A micro manager that contains the document context
 *
 * This will grow in the future if we implement bokeh.io.push_notebook
 */
var ContextManager = /** @class */ (function () {
    function ContextManager(context) {
        this._context = context;
    }
    Object.defineProperty(ContextManager.prototype, "context", {
        get: function () {
            return this._context;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(ContextManager.prototype, "isDisposed", {
        get: function () {
            return this._context === null;
        },
        enumerable: true,
        configurable: true
    });
    ContextManager.prototype.dispose = function () {
        if (this.isDisposed) {
            return;
        }
        this._context = null;
    };
    return ContextManager;
}());
exports.ContextManager = ContextManager;
