import {BENCH, RootStateMaybe, RUN} from "../index";
import React, {useState, useEffect} from 'react';
import { useDispatch, useSelector} from 'react-redux';

import {
    IonProgressBar,
    IonCard,
    IonCardContent,
    IonRow,
    IonGrid,
    IonButton,
    IonCol
} from "@ionic/react";
import {addViewProgram} from "../actions";
import {RowFunctionImage} from "./RowFunctionImage";
import {SERVER} from "../constants";

const NONE = 'none';
const BLOCK = 'block';

interface ResponseBenchmark {index: number, time: number}

const defaultCompare = ( x: number, y: number ):number => {
    if( x === undefined && y === undefined )
        return 0;

    if( x === undefined )
        return 1;

    if( y === undefined )
        return -1;

    if( x < y )
        return -1;

    if( x > y )
        return 1;

    return 0;
};


export const PerformaceView: React.FC = () => {

    const [display, setDisplay] = useState<string>("none");
    let numberView = useSelector((state: RootStateMaybe) => state.view.num);
    let typeView = useSelector((state: RootStateMaybe) => state.view.type);
    useEffect(
        ()=> {
            if (typeView === BENCH)
                setDisplay("block");
            else
                setDisplay("none");
        }
        ,[typeView, numberView])

    let [benchmarks, setBenchmarks] = useState<any[]>([]);
    let [valueProgressBar, setValueProgressBar] = useState<number>(0);
    let [imm, setImm] = useState<boolean>(false)
    let programs = useSelector((state: RootStateMaybe) => state.programs);
    let program = '';
    programs.forEach(p => {
        program +=  p
    })
    let tests = useSelector((state: RootStateMaybe) => state.testcases);
    let numberOfTests:number = tests.length;

    useEffect(()=> {
            if (valueProgressBar === 1) {
                setImm(true);
            } else setImm(false);
        }
        ,[valueProgressBar]);

    return(
        <div style={{display:display}}>
            <IonCard>
                <IonCardContent>
                    <IonRow>
                        <IonCol size={"3"}>
                            <IonButton expand="full" onClick={e=>{

                                setBenchmarks([]);
                                const actuallyBenchmarks:ResponseBenchmark[] = [];
                                const calcBenchmark = (test: string, index: number) => {
                                    new Promise(() => $.ajax({
                                        url: SERVER + 'benchmark/',
                                        type: 'POST',
                                        dataType: 'json',
                                        async: true,
                                        contentType: "application/json; charset=utf-8",
                                        data: JSON.stringify({programs: program, test, testIndex: index}),
                                        success: (data: ResponseBenchmark ) => {
                                            let array: ResponseBenchmark[] = actuallyBenchmarks;
                                            array.push(data);
                                            array.sort((a, b) => {
                                                return defaultCompare(a.index, b.index)
                                            })
                                            setBenchmarks(actuallyBenchmarks);
                                            if(numberOfTests !== 0) {
                                                setValueProgressBar(array.length / numberOfTests);
                                            }

                                        },
                                        error: () => {

                                        }
                                    }).then(
                                        () => {

                                        }
                                    )
                                    )
                                }
                                new Promise(()=>
                                    tests.forEach(
                                        (test: any, index: number) => {
                                            if (test) {
                                                calcBenchmark(test, index)
                                            }
                                        }
                                    )).then(() => setValueProgressBar(1))
                                }
                                }>RUN PERFORMANCE ANALYSIS</IonButton>
                        </IonCol>
                        <IonCol>
                            <IonProgressBar type="determinate" value={valueProgressBar} style={
                            {display: valueProgressBar===0?NONE:BLOCK}}/>
                        </IonCol>
                    </IonRow>
                    <IonRow>
                        <IonGrid>
                            <IonRow>
                                <IonCol>
                                    Testcase
                                </IonCol>
                                <IonCol>
                                    Timing
                                </IonCol>
                            </IonRow>


                                {
                                    benchmarks.map((b, i: number)=> {
                                        return (
                                            <div key={i}>
                                                <IonRow>
                                                    <IonCol>{b.index + 1}</IonCol>
                                                    <IonCol>{b.time}</IonCol>
                                                </IonRow>
                                            </div>)
                                        }
                                    )
                                }


                        </IonGrid>
                    </IonRow>
                        <RowFunctionImage benchmarks={benchmarks} tests={tests} active={imm}/>

                </IonCardContent>
            </IonCard>
        </div>
    )
}