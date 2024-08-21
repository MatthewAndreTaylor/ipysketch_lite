import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

declare global {
  interface Window {
    sendMessage: (message: string) => Promise<void>;

    saveLastMessage: (fileName: string) => Promise<void>;
  }

  let lastMessage: string;
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

      lastMessage = message;
    };

    window.saveLastMessage = async (path: string) => {
      console.log('saving content');

      if (!lastMessage) {
        console.error('No content to save');
        return;
      }

      const dataURI = lastMessage;
      const byteString = atob(dataURI.split(',')[1]);
      const type = dataURI.match(/:(.*?);/)![1];
      const array = new Uint8Array(byteString.length);
      for (let i = 0; i < byteString.length; i++) {
        array[i] = byteString.charCodeAt(i);
      }

      // send the message to the python
      await app.serviceManager.contents.save(path, {
        type: 'file',
        content: new Blob([array], { type: type })
      });
    };
  }
};

export default plugin;

//conda activate jupyterlab-ext

// jlpm run build
// jupyter lab
