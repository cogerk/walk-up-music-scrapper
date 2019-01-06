import { DocumentRegistry } from '@jupyterlab/docregistry';
import { INotebookModel, NotebookPanel } from '@jupyterlab/notebook';
import { JupyterLabPlugin } from '@jupyterlab/application';
import { IDisposable } from '@phosphor/disposable';
export declare type INBWidgetExtension = DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel>;
export declare class NBWidgetExtension implements INBWidgetExtension {
    createNew(nb: NotebookPanel, context: DocumentRegistry.IContext<INotebookModel>): IDisposable;
}
export declare const extension: JupyterLabPlugin<void>;
