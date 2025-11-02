import {IonButton, IonMenuButton, IonHeader, IonItem, IonToolbar, IonContent, IonList, IonMenu, IonTitle, IonRouterOutlet} from "@ionic/react";
import React, {useState, useEffect} from 'react';
import { useSelector } from 'react-redux';
import {ButtonAddMenu} from "./ButtonAddMenu";
import {ProgramMenuItem} from './ProgramMenuItem'
import {PROGRAM, TEST, RUN, BENCH, RootStateMaybe} from "../index";

export const Menu: React.FC = () => {
    let programsNumber = useSelector((state: RootStateMaybe) => state.programsNumber);
    let testsNumber = useSelector((state: RootStateMaybe) => state.testsNumber);

    return (
        <>
            <IonMenu side="end" contentId="main">
                <IonHeader>
                    <IonToolbar color="secondary">
                        <ButtonAddMenu/>
                        <IonMenuButton slot="end"/>
                    </IonToolbar>
                </IonHeader>
                <IonContent id="main">
                    <IonList>
                        {
                            Array.from(Array(programsNumber), (e, i) => {
                                return <div key={i}><ProgramMenuItem name="Program" type={PROGRAM} num={i+1}/></div>
                        })}
                        {
                            Array.from(Array(testsNumber), (e, i) => {
                                return <div key={i + programsNumber}><ProgramMenuItem name="Test" type={TEST} num={i+1}/></div>
                        })}
                        <div key={0 + programsNumber + testsNumber}><ProgramMenuItem name="RUN" type={RUN} num={0}/></div>
                        <div key={1 + programsNumber + testsNumber}><ProgramMenuItem name="BENCHMARKS" type={BENCH} num={0}/></div>
                    </IonList>
                </IonContent>
            </IonMenu>
        </>
    );
}