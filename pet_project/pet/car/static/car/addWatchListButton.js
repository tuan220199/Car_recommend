'use strict';

const e = React.createElement;

function AddWatchListButton(props){
    
    const [buttonClicked, setButtonClicked] = React.useState(false);
    const user_id = props.user_id;
    
    function add_to_watchList(car_id_pass){
        const data = {"user_watch_list_id": user_id, "car_id": car_id_pass};
            fetch(`/watch_list/add/api/${user_id}/`, {
                    method: "POST",
                    headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": window.csrfToken
                    },
                    body: JSON.stringify(data)
                })
                .then(response => {
                    if (!response.ok) {
                    throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    console.log(data);
                })
                .catch(error => {
                    console.error('There was an error!', error);
                });
        setButtonClicked(true);
    }

    function remove_to_watchList(car_id_pass){
        const data = {"user_watch_list_id": user_id, "car_id": car_id_pass};
            fetch(`/watch_list/remove/api/${user_id}/`, {
                    method: "POST",
                    headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": window.csrfToken
                    },
                    body: JSON.stringify(data)
                })
                .then(response => {
                    if (!response.ok) {
                    throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    console.log(data);
                })
                .catch(error => {
                    console.error('There was an error!', error);
                });
        setButtonClicked(true);
    }

    React.useEffect(() => {
        
        // Additional logic or actions after button click
        props.fetchWatchListData(); // Fetch updated watch list data
        setButtonClicked(false); // Reset buttonClicked state after re-render
        
        }, [buttonClicked]);

    return (
       <React.Fragment>
            {props.checkState ? (
                <button class="btn btn-default w-100 mb-md-0 mb-3 mr-md-3 mr-0" onClick={() => remove_to_watchList(props.car_id)}><i class='fas fa-check'></i> Already added to watch list</button>
            )
            :
            (
                <button class="btn btn-default w-100 mb-md-0 mb-3 mr-md-3 mr-0" onClick={() => add_to_watchList(props.car_id)}><i class='fas fa-plus'></i> Add to watch list</button>
            )
            }
       </React.Fragment>
    );
  }

