import { IDisposable } from '@phosphor/disposable';
import { DocumentRegistry } from '@jupyterlab/docregistry';
/**
 * A micro manager that contains the document context
 *
 * This will grow in the future if we implement bokeh.io.push_notebook
 */
export declare class ContextManager implements IDisposable {
    private _context;
    constructor(context: DocumentRegistry.IContext<DocumentRegistry.IModel>);
    readonly context: DocumentRegistry.IContext<DocumentRegistry.IModel>;
    readonly isDisposed: boolean;
    dispose(): void;
}
