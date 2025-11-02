import {ProgramView} from '../components/ProgramView';
import React, {useState, useEffect} from 'react';
import { useSelector } from 'react-redux';
import { RootStateMaybe } from '..';
import {RunningView} from "./RunningView";
import {PerformaceView} from "./PerformanceView";
import { IonRouterOutlet, IonMenu, IonContent, IonList, IonButton, IonHeader, IonToolbar, IonItem, IonTitle } from '@ionic/react';


export const ProgramManager: React.FC = 
(
    {children}
) => {
    
    let programsNumber = useSelector((state: RootStateMaybe) => state.programsNumber);
    let testsNumber = useSelector((state: RootStateMaybe) => state.testsNumber); 

    const PROGRAM = 'Program ';
    const TEST_CASE = 'Test-case ';

    interface ProgramViewProps{
        key: number, title:string, isTest:boolean
    }


    let arrayProgram:ProgramViewProps[] = [];
    for(let i: number = 1; i <= programsNumber; i++){
        arrayProgram.push({key: i, title:PROGRAM + i, isTest:false});
    }

    for(let i: number = 1; i <= testsNumber; i++){
        arrayProgram.push({key: i, title:TEST_CASE + i, isTest:true});
    }
    
    return(
        <>
        {
            arrayProgram.map((e, i) => {

            return (<ProgramView key={i} title={e.title} isTest={e.isTest} code={e.key}/>)
            })
        }

        <RunningView/>
        <PerformaceView/>

        </>
    );
}