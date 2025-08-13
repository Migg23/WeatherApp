
import {useState , useEffect} from "react"


function TemperatureDisplay(){
    const [temper , setTemper] = useState(0);
    const [curTime , setTime] = useState(0);
    const [timeZn , setTimeZn] = useState(null);

    


    const getTemperature = async () =>{
        try{
            const response = await fetch('http://localhost:5000/temp-time');

            const data = await response.json();

            setTemper(data.temperature);
            setTime(data.time);
            setTimeZn(data.timezone);
        }
        catch(ex){
            alert("Cannot get information" )
        }
        

        
    }
    
    return(
        <div>
            <h2>{timeZn}</h2>
            <p>
                {curTime}
            </p>
            <p>
                {temper}
            </p>
            <p>This works</p>
        </div>
    );
}


export default TemperatureDisplay