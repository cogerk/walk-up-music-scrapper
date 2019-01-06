import { IRenderMime } from '@jupyterlab/rendermime-interfaces';
import { KernelMessage, Kernel } from '@jupyterlab/services';
import { Widget } from '@phosphor/widgets';
import { ContextManager } from './manager';
export declare interface KernelProxy {
    registerCommTarget(targetName: string, callback: (comm: Kernel.IComm, msg: KernelMessage.ICommOpenMsg) => void): void;
}
export declare const BOKEHJS_LOAD_MIME_TYPE = "application/vnd.bokehjs_load.v0+json";
export declare const BOKEHJS_EXEC_MIME_TYPE = "application/vnd.bokehjs_exec.v0+json";
/**
 * Load BokehJS and CSS into the DOM
 */
export declare class BokehJSLoad extends Widget implements IRenderMime.IRenderer {
    private _load_mimetype;
    private _script_element;
    constructor(options: IRenderMime.IRendererOptions);
    renderModel(model: IRenderMime.IMimeModel): Promise<void>;
}
/**
 * Exec BokehJS in window
 */
export declare class BokehJSExec extends Widget implements IRenderMime.IRenderer {
    private _manager;
    private _html_mimetype;
    private _js_mimetype;
    private _exec_mimetype;
    private _script_element;
    private _server_id;
    private _document_id;
    constructor(options: IRenderMime.IRendererOptions, manager: ContextManager);
    readonly isDisposed: boolean;
    renderModel(model: IRenderMime.IMimeModel): Promise<void>;
    dispose(): void;
}
