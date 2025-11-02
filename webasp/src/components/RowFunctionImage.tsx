import {RootStateMaybe} from "../index";
import React, {useState, useEffect} from 'react';
import { useDispatch, useSelector} from 'react-redux';
import {
    IonProgressBar,
    IonCard,
    IonCardContent,
    IonRow,
    IonGrid,
    IonButton,
    IonCol,
    IonImg
} from "@ionic/react";
import {SERVER} from "../constants";

export const RowFunctionImage: React.FC<{benchmarks: number[], tests: string[], active: boolean}> = ({children, benchmarks, tests, active}) => {
    const [urlImage, setUrlImage] = useState<string>('');
    const [changeIm, setChangeIm] = useState<boolean>(true);

    useEffect(()=>{
        if(benchmarks.length === tests.length && benchmarks.length>0){
            $.ajax(
                {
                    url: SERVER + 'performace/',
                    type: 'POST',
                    dataType: 'json',
                    async: true,
                    contentType: "application/json; charset=utf-8",
                    data: JSON.stringify({tests, benchmarks}),
                    success: (data: {url:string}) => {
                        setUrlImage(SERVER + data['url']);
                        setChangeIm(!changeIm)
                    },
                    error: (data) => {
                        console.log(' 1n')
                    }
                }
            )
        }},[active])

    if(urlImage !== '' && active)
        return (
            <div>
                <IonRow>
                    <IonCol>
                        <IonImg src={changeIm? urlImage: urlImage}/>
                    </IonCol>
                </IonRow>
            </div>
        )
    else return (<div></div>);
}