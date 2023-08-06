import React from 'react';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Switch from '@material-ui/core/Switch';
import { makeStyles } from '@material-ui/core/styles';

interface IToggleProps {
  clickHandler1: () => void;
  clickHandler2: () => void;
  clickHandler3: () => void;
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
      alignItems: 'center',
      marginLeft: '100px'
    }
  }));
  const classes = useStyles();

  const [state, setState] = React.useState({
    checkedA: false,
    checkedB: true,
    checkedC: true
  });

  const handleChange1 = (event: React.ChangeEvent<HTMLInputElement>) => {
    setState({ ...state, [event.target.name]: event.target.checked });
    Props.clickHandler1();
  };

  const handleChange2 = (event: React.ChangeEvent<HTMLInputElement>) => {
    setState({ ...state, [event.target.name]: event.target.checked });
    Props.clickHandler2();
  };

  const handleChange3 = (event: React.ChangeEvent<HTMLInputElement>) => {
    setState({ ...state, [event.target.name]: event.target.checked });
    Props.clickHandler3();
  };

  return (
    <div>
      <FormGroup className={classes.formGroup} row>
        <FormControlLabel
          control={
            <Switch
              checked={state.checkedA}
              onChange={handleChange1}
              name="checkedA"
            />
          }
          label="Toggle Spin"
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
          label="Alpha"
        />
        <FormControlLabel
          control={
            <Switch
              checked={state.checkedC}
              onChange={handleChange3}
              name="checkedC"
              color="secondary"
            />
          }
          label="Beta"
        />
      </FormGroup>
    </div>
  );
}
