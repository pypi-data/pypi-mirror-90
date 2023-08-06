import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

/**
 * Initialization data for the jupyterlab-rwth extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab-rwth',
  autoStart: true,
  activate: (app: JupyterFrontEnd) => {
    console.log('JupyterLab extension jupyterlab-rwth is activated!');
  }
};

export default extension;
