// Copyright (c) Jupyter Development Team
// Distributed under the terms of the Modified BSD License.

import {
  Application, /*IPlugin*/
} from '@phosphor/application';

import {
  Widget
} from '@phosphor/widgets';

import {
  IJupyterWidgetRegistry
 } from '@jupyter-widgets/base';

import * as scales from './widgets';

import {
  MODULE_NAME, MODULE_VERSION
} from './version';

import '../styles/plugin.css';

const EXTENSION_ID = 'jupyter-scales:plugin';

/**
 * The example plugin.
 */
const plugin: any /* IPlugin<Application<any >, void>  Only until phosphor -> lumino rename is completed */ = {
  id: EXTENSION_ID,
  requires: [IJupyterWidgetRegistry],
  activate: activateWidgetExtension,
  autoStart: true
};

export default plugin;


/**
 * Activate the widget extension.
 */
function activateWidgetExtension(app: Application<Widget>, registry: IJupyterWidgetRegistry): void {
  registry.registerWidget({
    name: MODULE_NAME,
    version: MODULE_VERSION,
    exports: scales,
  });
}
