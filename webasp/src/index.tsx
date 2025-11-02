import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import * as serviceWorkerRegistration from './serviceWorkerRegistration';
import reportWebVitals from './reportWebVitals';
import {storeReducer} from './reducer';
import { Provider } from 'react-redux';


import {createStore, combineReducers} from 'redux';

interface SyntAnalysis {
    aggregateLiterals: number,
    classicalRule: number,
    constraintRules: number,
    disjuntiveRule: number,
    facts: number,
    rules: number,
    variables: number,
    weakConstraints: number
}

export interface RootStateMaybe {
  programs: string[],
  testcases: string[],
  programsNumber: number,
  testsNumber: number,
    view: {
        type: string,
        num: number
    }
}

export const PROGRAM = "program";
export const TEST = "test";
export const RUN = "run";
export const BENCH = "bench";


var storeProgram: RootStateMaybe = {
    programs: [],
    testcases: [],
    programsNumber: 1,
    testsNumber: 0,
    view: {
        type: PROGRAM,
        num: 1
    }
};

let store = createStore(storeReducer, storeProgram);

ReactDOM.render(
  <Provider store={store}>
  <React.StrictMode>
    <App />
  </React.StrictMode>
  </Provider>,
  document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://cra.link/PWA
serviceWorkerRegistration.unregister();

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
