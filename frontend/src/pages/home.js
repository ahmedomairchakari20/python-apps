import '../styles/home.css'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faCircleArrowLeft, faAddressCard, faListCheck, faTableColumns, faMagnifyingGlassChart, faCalendar, faGear } from '@fortawesome/free-solid-svg-icons'
import { Link } from 'react-router-dom'
import { useContext ,useEffect,useState} from 'react'
import AuthContext from '../lib/authcontext'
import { useNavigate } from 'react-router-dom'

const api = {
    key: "32d3ed0c182955f0de323193f015dfc8",
    base: "https://api.openweathermap.org/data/2.5/",
  };

function Home(){

    const { authenticated, setAuthenticated } = useContext(AuthContext);

    const navigate = useNavigate ();

    async function logoutHandler(){
        localStorage.setItem('loggedEmail', '')
        setAuthenticated(false)
        navigate('/')
    }
    const [search, setSearch] = useState("dublin");
    const [weather, setWeather] = useState({});

    /*
        Search button is pressed. Make a fetch call to the Open Weather Map API.
    */
    const searchPressed = () => {
            fetch(`${api.base}weather?q=${search}&units=metric&APPID=${api.key}`)
            .then((res) => res.json())
            .then((result) => {
                setWeather(result);
            });
        };
    useEffect(() => {
       
        searchPressed();
    }, [search]);
    return(
        <div className='home-container'>
            <div className='container'style={{background:"none"}}>
                <div className="row">
                
                    <div className='col-lg-8'>
                        <div className='logoutIcon'>
                        <FontAwesomeIcon
                            className="itemright"
                            size="2xl"
                            icon={faCircleArrowLeft}
                            style={{ color: "#ffffff" }}
                            onClick={logoutHandler}
                        /> Log out
                        </div>
                        <div className='d-flex justify-content-center'>
                            <h2>Home</h2>
                        </div>
                        <div className='container home-items-container'>
                            <Link style={{color:"white"}} to={'/profile'} className='home-items'>
                                {/* <div className='home-items'> */}
                                <FontAwesomeIcon size='2xl' icon={faAddressCard} />
                                <h4>Profile</h4>
                                {/* </div> */}
                            </Link>
                            <Link style={{color:"white"}} to={'/tasks'} className='home-items'>
                                <FontAwesomeIcon size='2xl' icon={faListCheck} />
                                <h4>Tasks</h4>
                            </Link>
                            <Link style={{color:"white"}} to={'/dashboard'} className='home-items'>
                                <FontAwesomeIcon size='2xl' icon={faTableColumns} />
                                <h4>Dashboard</h4>
                            </Link>
                            
                        </div>
                    </div>
                    <div className='col-lg-4'>
                        <div className='weather-side'>
                            <div className="App">
                                <header className="App-header">
                                    <h2>Weather forcast</h2>
                                    <div className='d-flex flex-row'>
                                    <input
                                        type="text"
                                        placeholder="Enter city/town..."
                                        onChange={(e) => setSearch(e.target.value)}
                                    />
                                    <button className='mt-4 btn btn-success rounded' style={{height:"fit-content"}} onClick={searchPressed}>Search</button>
                                    </div>

                                    {/* If weather is not undefined display results from API */}
                                    {typeof weather.main !== "undefined" ? (
                                    <div style={{paddingLeft:"2rem"}}>
                                        {/* Location  */}
                                        <p style={{marginBottom:"0.5rem"}}>{weather.name}</p>

                                        {/* Temperature Celsius  */}
                                        <p style={{marginBottom:"0.5rem"}}>{weather.main.temp}°C</p>

                                        {/* Condition (Sunny ) */}
                                        <p style={{marginBottom:"0.5rem"}}>{weather.weather[0].main}</p>
                                        <p style={{marginBottom:"0.5rem"}}>({weather.weather[0].description})</p>
                                    </div>
                                    ) : (
                                    ""
                                    )}
                                </header>
                            </div>
                        </div>
                        <div className='news'>
                            <h2>News</h2>
                            <iframe src="https://www.irishtimes.com/" width="100%" height="318" ></iframe>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Home