import {IonButton, IonAlert, IonMenuButton} from "@ionic/react";
import React, {useState, useEffect} from 'react';
import { useDispatch } from 'react-redux';
import { addViewProgram } from '../actions';


export const ButtonAddMenu: React.FC = () => {
    const dispatch = useDispatch();

    const [showAlert, setShowAlert] = useState<boolean>(false);
    const onClickAlert = (e: any) => {
        setShowAlert(true)
    };

    return (<>
        <IonMenuButton slot="primary" color="light" onClick={onClickAlert}>+</IonMenuButton>
        <IonAlert
          isOpen={showAlert}
          onDidDismiss={() => setShowAlert(false)}
          header={'Alert'}
          subHeader={'Subtitle'}
          message={'This is an alert message.'}
          buttons={[
              {
                  text: 'Cancel',
                  role: 'cancel'
              },
              {
                  text:'Add program',
                  handler: () => {
                      dispatch(addViewProgram(false));
                  }
              },
              {
                  text:'Add Test-case',
                  handler: () => {
                      dispatch(addViewProgram(true));
                  }
              }
              ]}
        />
        </>);
}