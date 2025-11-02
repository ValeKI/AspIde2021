import {IonItem ,IonButton, IonLabel} from "@ionic/react";
import React, {useState, useEffect} from 'react';
import { useDispatch } from 'react-redux';
import {addProgram, changeView} from "../actions";
import {BENCH, RUN, PROGRAM} from "../index";

export const ProgramMenuItem: React.FC<{name: string, type: string, num: number}> = ({children, name, type, num}) => {
    const dispatch = useDispatch();

    const onClickLabel = () => {
        console.log('o');
        dispatch(changeView(type, num));
    }
    const [buttonsFunz, setButtons] = useState<JSX.Element>(<></>);

    useEffect(()=>
    {
        if(type !== RUN && type !== BENCH){
            setButtons(<div><IonButton>ok</IonButton><IonButton>no</IonButton></div>);
        }
    },[type])


    return (
        <>
        <IonItem>
            <IonButton expand="full" onClick={onClickLabel}>{name}</IonButton>
            {buttonsFunz}
        </IonItem>
        </>
    )
}