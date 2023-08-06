import { ReactWidget } from '@jupyterlab/apputils';

import React from 'react';

import * as NGL from 'ngl';

import Button from '@material-ui/core/Button';

import * as _ from 'underscore';

import VerticalSlider from './sliders';
import SwitchLabels from './switches';

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

    const stage = new NGL.Stage(this.uuid, { backgroundColor: 'black' });

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

    stage
      .loadFile('data://benzene.sdf', { name: 'structure1' })
      .then((o: any) => {
        const atomTriple = [[0, 1, 2]];

        o.addRepresentation('ball+stick');

        o.addRepresentation('label', {
          labelType: 'atomindex',
          color: 'white'
        });

        o.addRepresentation('angle', {
          atomTriple: atomTriple,
          labelSize: 1.0,
          labelColor: 'yellow',
          sdf: false
        });

        o.autoView();
      });

    stage
      .loadFile('data://benzene-homo.cube', { name: 'surface_1' })
      .then((o: any) => {
        o.addRepresentation('surface', {
          visible: true,
          isolevelType: 'value',
          isolevel: 0.01,
          color: 'blue',
          opacity: 0.7,
          opaqueBack: false
        });

        o.signals.visibilityChanged.add((value: any) => {
          console.log('Dou Du****:' + value);
        });

        o.autoView();
      });

    stage
      .loadFile('data://benzene-homo.cube', { name: 'surface_2' })
      .then((o: any) => {
        o.addRepresentation('surface', {
          visible: true,
          isolevelType: 'value',
          isolevel: -0.01,
          color: 'red',
          opacity: 0.7,
          opaqueBack: false
        });
        o.autoView();
      });

    this.stage = stage;
  }

  updateIsosurface(e: number) {
    this.stage
      .getRepresentationsByName('surface')
      .setParameters({ opacity: e });

    this.stage.getComponentsByName('surface_1').list[0].setVisibility(true);
    this.stage.getComponentsByName('surface_2').list[0].setVisibility(true);
  }

  updateIsolevel(e: number, filename: string) {
    this.stage
      .getComponentsByName(filename)
      .list[0].eachRepresentation((reprElem: any) => {
        reprElem.setParameters({ isolevel: e });
      });
  }

  toggleVisibility(filename: string) {
    const a = this.stage.getComponentsByName(filename).list[0];
    a.setVisibility(!a.visible);
  }

  setVisibility(filename: string, val: boolean) {
    const a = this.stage.getComponentsByName(filename).list[0];
    a.setVisibility(val);
  }

  toggleSpin() {
    this.stage.toggleSpin();
  }

  render(): JSX.Element {
    const func1 = (): void => this.stage.toggleSpin();
    const func2 = (): void => this.toggleVisibility('surface_1');
    const func3 = (): void => this.toggleVisibility('surface_2');

    return (
      <div>
        <div style={{ width: '30%' }}>
          <VerticalSlider
            uuid={this.uuid}
            changeHandler1={(
              event: React.ChangeEvent<{}>,
              val: number | number[]
            ): void => {
              const value = (val as number) / 100.0;
              this.updateIsosurface(value);
            }}
            changeHandler2={(
              event: React.ChangeEvent<{}>,
              val: number | number[]
            ): void => {
              const value = val as number[];
              this.updateIsolevel(value[0], 'surface_1');
              this.updateIsolevel(value[1], 'surface_2');
            }}
          />
        </div>

        <div style={{ marginLeft: '200px', marginTop: '10px' }}>
          <Button
            color="primary"
            variant="contained"
            onClick={(): void => {
              this.toggleVisibility('surface_1');
              this.toggleVisibility('surface_2');
            }}
          >
            Toggle surface
          </Button>
          <Button
            style={{ marginLeft: '30px' }}
            color="secondary"
            variant="contained"
            onClick={(): void => {
              this.toggleVisibility('structure1');
            }}
          >
            Toggle structure
          </Button>
        </div>

        <SwitchLabels
          clickHandler1={func1}
          clickHandler2={func2}
          clickHandler3={func3}
        />
      </div>
    );
  }
}
