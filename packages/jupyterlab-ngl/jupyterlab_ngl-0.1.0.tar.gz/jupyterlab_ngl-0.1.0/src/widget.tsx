import { ReactWidget } from '@jupyterlab/apputils';

import React from 'react';

import * as NGL from 'ngl';

import Slider from '@material-ui/core/Slider';

import Button from '@material-ui/core/Button';

import * as _ from 'underscore';

import Switch from '@material-ui/core/Switch';

/**
 * A Counter Lumino Widget that wraps a CounterComponent.
 */
export class CounterWidget extends ReactWidget {
  /**
   * Constructs a new CounterWidget.
   */

  stage: any;
  uuid: string;

  constructor() {
    super();
    this.addClass('jp-ReactWidget');
    this.uuid = _.uniqueId('ngl_');

    window.requestAnimationFrame(() => {
      this.visualizer();
    });
  }

  visualizer() {
    NGL.DatasourceRegistry.add(
      'data',
      new NGL.StaticDatasource('//cdn.rawgit.com/arose/ngl/v2.0.0-dev.32/data/')
    );

    const stage = new NGL.Stage(this.uuid);

    window.addEventListener(
      'resize',
      event => {
        stage.handleResize();
      },
      false
    );

    stage.viewer.container.addEventListener('dblclick', () => {
      stage.toggleFullscreen();
    });

    stage.loadFile('data://1crn.pdb').then((o: any) => {
      o.addRepresentation('tube', { radius: 'sstruc' });
      o.addRepresentation('ball+stick', { sele: 'sidechainAttached' });
      o.addRepresentation('label', {
        sele: '.CA',
        color: 'element',
        labelType: 'format',
        labelFormat: '%(resname)s %(chainname)s%(resno)s'
      });
      o.autoView();
    });

    stage.loadFile('data://1crn.ply', { name: 'dou' }).then((o: any) => {
      o.addRepresentation('surface', {
        opacity: 0.3,
        side: 'front',
        color: 'red'
      });
    });

    this.stage = stage;
  }

  updateIsosurface(e: number) {
    this.stage
      .getRepresentationsByName('surface')
      .setParameters({ opacity: e });

    this.stage.getComponentsByName('dou').list[0].setVisibility(true);
  }

  toggleVisibility() {
    const a = this.stage.getComponentsByName('dou').list[0];
    a.setVisibility(!a.visible);
  }

  toggleSpin() {
    this.stage.toggleSpin();
  }

  render(): JSX.Element {
    const marks = [
      {
        value: 0,
        label: '0%'
      },
      {
        value: 50,
        label: '50%'
      },
      {
        value: 100,
        label: '100%'
      }
    ];

    return (
      <div>
        <div
          id={this.uuid}
          style={{
            width: '800px',
            height: '500px',
            backgroundColor: 'black',
            margin: '0 auto'
          }}
        ></div>

        <div style={{ textAlign: 'center' }}>
          <Slider
            id="iso-slider"
            style={{ width: '500px' }}
            defaultValue={30}
            aria-labelledby="discrete-slider"
            valueLabelDisplay="auto"
            step={5}
            min={0}
            max={100}
            marks={marks}
            onChange={(event, val): void => {
              const value = (val as number) / 100.0;
              this.updateIsosurface(value);
            }}
          />
        </div>

        <div style={{ textAlign: 'center' }}>
          <Button
            color="primary"
            variant="contained"
            onClick={(): void => this.toggleVisibility()}
          >
            Show surface
          </Button>
        </div>

        <div style={{ textAlign: 'center' }}>
          <Switch
            checked={true}
            onChange={(): void => this.toggleSpin()}
            name="checkedA"
            inputProps={{ 'aria-label': 'secondary checkbox' }}
          />
        </div>
      </div>
    );
  }
}
