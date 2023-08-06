import { ReactWidget } from '@jupyterlab/apputils';

import React from 'react';

import * as NGL from 'ngl';

import Slider from '@material-ui/core/Slider';

import Button from '@material-ui/core/Button';

import * as _ from 'underscore';

import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Switch from '@material-ui/core/Switch';
import { makeStyles } from '@material-ui/core/styles';

interface IToggleProps {
  clickHandler1: () => void;
  clickHandler2: () => void;
}

export default function SwitchLabels(Props: IToggleProps) {
  const useStyles = makeStyles(theme => ({
    container: {
      display: 'flex',
      flexWrap: 'wrap',
      position: 'absolute',
      top: 0,
      left: 0,
      height: '100%',
      width: '100%',
      alignItems: 'center'
    },
    textField: {
      marginLeft: theme.spacing(1),
      marginRight: theme.spacing(1),
      width: 200
    },
    formGroup: {
      alignItems: 'center'
    }
  }));
  const classes = useStyles();

  const [state, setState] = React.useState({
    checkedA: false,
    checkedB: false
  });

  const handleChange1 = (event: React.ChangeEvent<HTMLInputElement>) => {
    setState({ ...state, [event.target.name]: event.target.checked });
    Props.clickHandler1();
  };

  const handleChange2 = (event: React.ChangeEvent<HTMLInputElement>) => {
    setState({ ...state, [event.target.name]: event.target.checked });
    Props.clickHandler2();
  };

  return (
    <div>
      <FormGroup className={classes.formGroup}>
        <FormControlLabel
          control={
            <Switch
              checked={state.checkedA}
              onChange={handleChange1}
              name="checkedA"
            />
          }
          label="Secondary"
        />
        <FormControlLabel
          control={
            <Switch
              checked={state.checkedB}
              onChange={handleChange2}
              name="checkedB"
              color="primary"
            />
          }
          label="Primary"
        />
      </FormGroup>
    </div>
  );
}

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

    const func1 = (): void => this.stage.toggleSpin();
    const func2 = (): void => this.stage.toggleFullscreen();

    return (
      <div>
        <div
          id={this.uuid}
          style={{
            width: '800px',
            height: '450px',
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

        <SwitchLabels clickHandler1={func1} clickHandler2={func2} />
      </div>
    );
  }
}
