import {IonButtons, IonContent, IonHeader, IonMenuButton, IonPage, IonTitle, IonToolbar} from '@ionic/react';
import './Home.css';
import { ProgramManager } from '../components/ProgramManager';
import React from "react";
import {ButtonAddMenu} from "../components/ButtonAddMenu";

const Home: React.FC = () => {
  return (
    <IonPage id="main-content">
      <IonHeader>
        <IonToolbar>
            <ButtonAddMenu/>
            <IonMenuButton slot="end"/>
                <IonTitle>ASPmarks</IonTitle>

        </IonToolbar>
      </IonHeader>
      <IonContent fullscreen>
        <IonHeader collapse="condense">
          <IonToolbar>
              <IonTitle size="large">ASPmarks</IonTitle>
          </IonToolbar>
        </IonHeader>
        <ProgramManager/>
      </IonContent>
    </IonPage>
  );
};

export default Home;
