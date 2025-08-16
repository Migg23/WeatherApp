import { useState , useEffect } from "react";


function HourlyTempDisplay(){

    const [allTemps , setAllTemps] = useState([]);


    useEffect(() =>{

        const FetchHourlyTemps = async ()=> {
            try{
                const response = await fetch('http://localhost:5000/index');
                const data = await response.json();

                setAllTemps(data);
            }
            catch(ex){
                alert("an error occured twin: " + ex);
            }
            
        }

        FetchHourlyTemps();
    })




    return(
        <div>
            <div>
                <p>
                    {allTemps.map((item , index) => {
                        return <p key={index}>{item}</p>
                    })}
                </p>
            </div>
        </div>
    );
}

export default HourlyTempDisplay