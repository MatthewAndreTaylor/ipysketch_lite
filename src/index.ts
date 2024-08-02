import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

declare global {
  interface Window {
    sendMessage: (message: string) => Promise<void>;
  }
}

/**
 * The plugin for sending messages to the python
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'ipysketch:plugin',
  autoStart: true,
  activate: (app: JupyterFrontEnd) => {
    console.log('ipysketch plugin activated');

    window.sendMessage = async (message: string) => {
      console.log('sending message');
      // send the message to the python
      await app.serviceManager.contents.save('message.txt', {
        type: 'file',
        format: 'text',
        content: message
      });
    };
  }
};

export default plugin;

//conda activate jupyterlab-ext

// jlpm run build
// jupyter lab
