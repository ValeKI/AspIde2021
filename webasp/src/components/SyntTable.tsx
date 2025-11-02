import React, {useState, useEffect} from 'react';
import { IonRow, IonCol, IonGrid } from '@ionic/react';
import {addProgram, clearProgram} from "../actions";
import {SERVER} from "../constants";

const WEAK_CONSTRAINT = 'weak_constraint'
const VARIABLE = 'variable'
const STATEMENT = 'statement'
const FACT = 'fact'
const DISJUNCTION = 'disjunction'
const CONSTRAINT_RULE = 'constraint_rule'
const CLASSICAL_RULE = 'classical_rule'
const AGGREGATE_FUNCTION = 'aggregate_function'

const keys = ['weak_constraint',
'variable',
'statement',
'fact',
'disjunction',
'constraint_rule',
'classical_rule',
'aggregate_function',
]


interface constructsCounter{
    'weak_constraint': number,
    'variable': number,
    'statement': number,
    'fact': number,
    'disjunction': number,
    'constraint_rule': number,
    'classical_rule': number,
    'aggregate_function': number,
}

export const SyntTable: React.FC<{text: any, isReload: boolean}> = ({children, text, isReload}) =>{
    const [reload, setReload] = useState<boolean>(isReload);
    const [counter, setCounter] = useState<constructsCounter>({
        'weak_constraint': 0,
        'variable': 0,
        'statement': 0,
        'fact': 0,
        'disjunction': 0,
        'constraint_rule': 0,
        'classical_rule': 0,
        'aggregate_function': 0
    })
    const setCounterConstruct = (construct: keyof constructsCounter, num: number) => {
        let c = {...counter}
        c[construct] = num;
        setCounter(c);
        console.log(c);
        console.log(construct);
        console.log(num);
    }
    // console.log('ups', isReload);

    useEffect(() => {

        if(text) {
            $.ajax(
                {
                    url: SERVER + 'syntAnalysis/',
                    type: 'POST',
                    dataType: 'json',
                    async: true,
                    contentType: "application/json; charset=utf-8",
                    data: JSON.stringify({text: text}),
                    success: (data) => {
                            let c = {...counter};
                            c[WEAK_CONSTRAINT] = data[WEAK_CONSTRAINT];
                            c[VARIABLE] = data[VARIABLE];
                            c[STATEMENT] = data[STATEMENT];
                            c[FACT] = data[FACT];
                            c[DISJUNCTION] = data[DISJUNCTION];
                            c[CONSTRAINT_RULE] = data[CONSTRAINT_RULE];
                            c[CLASSICAL_RULE] = data[CLASSICAL_RULE];
                            c[AGGREGATE_FUNCTION] = data[AGGREGATE_FUNCTION];
                            setCounter(c);
                    },
                    error: () => {
                    }
                }
            );
        }
        console.log('c statment', counter[FACT]);
    }, [isReload])


    return(
        <IonGrid class="ion-margin">
        <IonRow>
            {
                keys.map((e, i) => <IonCol key={i}>{e}</IonCol>)
            }
        </IonRow>
        <IonRow>
            {
                keys.map((e, i) => <IonCol key={i}>{counter[e as keyof constructsCounter]}</IonCol>)
            }
        </IonRow>
        </IonGrid>
    );

}