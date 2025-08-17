import { useState, useEffect } from "react";


function NextTempsDIsplay(){
    
    const [dayOneTemps , setDayOne] = useState([]);
    const [dayTwoTemps , setDayTwo] = useState([]);
    const [dayThreeTemps , setDayThree] = useState([]);


    useEffect(()=>{
        const FetchAllTemps = async ()=>{
            try{
                const response = await fetch('http://localhost:5000/upcoming-weather');
                const data = await response.json();

                setDayOne(data.dayOne);
                setDayTwo(data.dayTwo);
                setDayThree(data.dayThree);
            }
            catch(ex){
                alert("An error occured twin: " + ex);
            }
        }

        FetchAllTemps();
    }, [])
    


    return(
        <div>
            <div>
                <p>{dayOneTemps[0]} and {dayOneTemps[1]}</p>
            </div>
            <div>
                <p>{dayTwoTemps[0]} and {dayTwoTemps[1]}</p>
            </div>
            <div>
                <p>{dayThreeTemps[0]} and {dayThreeTemps[1]}</p>
            </div>
        </div>
    )
}

export default NextTempsDIsplay