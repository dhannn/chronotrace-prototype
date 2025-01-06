import React from 'react'
import { Scanner } from '@yudiel/react-qr-scanner'

const App = () => {
    return (
        <div>
            <h1 id='id-numh1'>ID Number:</h1>
            <input id='id-num' type='text'/>
            <h1 id='greetings'></h1>
            <h2 id='timestamp'></h2>
            <Scanner onScan={async (result) => {

                const idnum = document.getElementById('id-num')
                const idnumh1 = document.getElementById('id-numh1')
                idnum.style = 'display: none;'
                idnumh1.style = 'display: none;'

                const id = idnum.value;
                const res = JSON.parse(result[0].rawValue.replaceAll("\'", "\""));

                // const IP_ADDRESS = `https://192.168.0.23:5000/log/${id}/token/${res['token']}`;
                const IP_ADDRESS = `https://10.254.133.34:5000/log/${id}/token/${res['token']}`;
                const response = await fetch(new URL(IP_ADDRESS), {
                    method: 'POST',
                    mode: 'cors'
                })

                const user_info = await response.json();
                const greetings = document.getElementById('greetings');
                const timestamp = document.getElementById('timestamp');
                if (user_info['entered']) {
                    greetings.innerText = `Welcome, ${user_info['name']}!`
                } else {
                    greetings.innerText = `Hope you had a productive day, ${user_info['name']}!`
                }
                timestamp.innerText = user_info['timestamp'];
            }}/>
        </div>
    )
}

export default App
