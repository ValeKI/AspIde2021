import { useDispatch, useSelector} from 'react-redux';
import React, {useState, useEffect} from 'react';
import {
    IonCard,
    IonCardContent,
    IonRow,
    IonButton,
    IonCol
} from "@ionic/react";
import {PROGRAM, RootStateMaybe, RUN, TEST} from "../index";
import {SERVER} from "../constants";

interface ResponseAnswerSets{ index: number, result: [] }

export const RunningView: React.FC = ({children}) => {
    const [answerset, setAnswerset] = useState<ResponseAnswerSets[]>([]);

    const [display, setDisplay] = useState<string>("none");
    let numberView = useSelector((state: RootStateMaybe) => state.view.num);
    let typeView = useSelector((state: RootStateMaybe) => state.view.type);
    useEffect(
        ()=> {
            if (typeView === RUN)
                setDisplay("block");
            else
                setDisplay("none");
        }
        ,[typeView, numberView])

    let programs = useSelector((state: RootStateMaybe) => state.programs);
    let program = '';
    programs.forEach(p => {
        program +=  p
    })
    let tests = useSelector((state: RootStateMaybe) => state.testcases);

    const getAnswerset = (program: any, tests: any) => {
        console.log('p1', tests);
        if(program){
            $.ajax(
                {
                    url: SERVER + 'answersets/',
                    type: 'POST',
                    dataType: 'json',
                    async: true,
                    contentType: "application/json; charset=utf-8",
                    data: JSON.stringify({'programs': program, 'tests': tests,
                        'testsIndex': tests.map((t: any, i: number) =>  {
                            if(t){
                                return i;
                            }
                        })}),
                    success: (data: { answersets: ResponseAnswerSets[] }) => {
                        console.log(data);
                            setAnswerset(data['answersets']);
                    },
                    error: () => {
                    }
                }
            )
        }
    }

    useEffect(()=>{},[answerset]);

    return (
        <div style={{display:display}}>
        <IonCard>
            <IonCardContent>
                {
                    answerset.map((answerset: ResponseAnswerSets, i:number) =>
                    {
                        if(answerset.index === 0)
                        {
                            return(
                            <div key={i}>
                            <h6>Only Program</h6>
                            <p>{answerset.result}</p>
                            </div>
                        )
                        }
                        return(
                            <div key={i}>
                            <h6>Testcase {answerset.index}: </h6>
                            <p>{answerset.result}</p>
                            </div>
                        )
                    })
                }
                <IonButton expand="full" onClick={e=>{getAnswerset(program, tests)}}>RUN</IonButton>
            </IonCardContent>
        </IonCard>
            </div>
                    );

}