import { IonRow, IonCol, IonLabel, IonCard, IonTextarea, IonItem, IonCardHeader, IonToolbar, IonCardTitle, IonCardContent, IonButton } from '@ionic/react';
import React, {useState, useEffect} from 'react';
import {addProgram, clearProgram} from '../actions';
import { useDispatch, useSelector } from 'react-redux';
import {PROGRAM, RootStateMaybe, TEST} from "..";
import $ from "jquery";
import {SyntTable} from "./SyntTable";
import {SERVER} from "../constants";


export const ProgramView: React.FC<{title: string, isTest: boolean, code:number}> = ({children, title, isTest, code}) => {
    const [text, setText] = useState<string>();
    const [display, setDisplay] = useState<string>("none");
    const [check, setCheck] = useState<number>(0);
    const [statusText, setStatusText] = useState<string>("");
    const [syntaxMessage, setSyntaxMessage] = useState<string>("");
    const [reloadSynt, setReloadSynt] = useState<boolean>(false);

   let numberView = useSelector((state: RootStateMaybe) => state.view.num);
   let typeView = useSelector((state: RootStateMaybe) => state.view.type);

    const empty = ""; // 0
    const syntaxError = "Syntax Error"; // 1
    const done = "Well done!"; // 2
    const netError = "Network Error!"; // 3

    const isCorrectASP = (text: string) =>{
        $.ajax(
            {
                url: SERVER + '/correctSynt/',
                type: 'POST',
                dataType: 'json',
                async: true,
                contentType: "application/json; charset=utf-8",
                data: JSON.stringify({"text": text}),
                success: (data) => {
                    if(data === true) {
                        dispatch(addProgram(text, isTest, numberProgram));
                        setCheck(2);
                    }
                    else {
                        setSyntaxMessage(data);
                        dispatch(addProgram(text, isTest, numberProgram));
                        dispatch(clearProgram(isTest, numberProgram));

                        setCheck(1);
                    }
                },
                error: () => {
                    setCheck(3);
                    dispatch(clearProgram(isTest, numberProgram));
                }
            }
        );
    }

    useEffect(
        ()=>{
            switch (check){
                case 0:
                    setStatusText(empty);
                    break;
                case 1:
                    setStatusText(syntaxError + ': ' + syntaxMessage);
                    break;
                case 2:
                    setStatusText(done);
                    break;
                case 3:
                    setStatusText(netError);
                    break;
            }
        }
        ,[check]);

    const dispatch = useDispatch();

    let numberProgram = code;

    useEffect(() => {
        if(reloadSynt){
            setReloadSynt(false);
        }
    },[reloadSynt] );

    useEffect(
        ()=> {
            if (((isTest && typeView === TEST) || (!isTest && typeView === PROGRAM)) && numberView === code)
                setDisplay("block");
            else
                setDisplay("none");
        }
        ,[typeView, numberView])

    return(
        <div style={{display: display}}>
        <IonCard>
            <IonCardHeader>
                <IonToolbar>
                    <IonCardTitle>{title}</IonCardTitle>
                </IonToolbar>
            </IonCardHeader>

            <IonCardContent>
              <IonItem>
                  <IonLabel position="floating">Asp Program</IonLabel>
                <IonTextarea value={text} rows={16} onIonChange={e =>
                {
                    setText(e.detail.value!);
                    setCheck(0);
                    setReloadSynt(true);
                }}/>
              </IonItem>
            </IonCardContent>
            <IonCardContent>
                <IonRow>
                    <IonCol>
                        <IonButton expand="full" onClick={e => 
                            {
                                if (text)
                                    isCorrectASP(text);
                            }}>Okay</IonButton>
                    </IonCol>
                    <IonCol>
                        {
                            statusText
                        }
                    </IonCol>
                    </IonRow>
            </IonCardContent>
            <SyntTable text={text} isReload={reloadSynt}/>
        </IonCard>
            </div>
    )
}
