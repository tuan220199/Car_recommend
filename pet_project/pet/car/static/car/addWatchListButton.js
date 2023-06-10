'use strict';

const e = React.createElement;

function AddWatchListButton(props){
    
    /* @param buttonClicked is to check whether the add to watch list is clicked or not in this component
     * (true: clicked, false: not click yet considered in this only 1 render time)
     * @param user_id is passed from parent component (as the current user)
     * @param isWatchListPage is passed from parent component (check if the parant component in watch list page (true) or not (false))
    */
    const [buttonClicked, setButtonClicked] = React.useState(false);
    const user_id = props.user_id;
    const isWatchListPage = props.isWatchListPage;
    
    //
    /**
     * The function adds a car to a user's watch list through a POST request to an API endpoint.
     * @param car_id_pass - The ID of the car that the user wants to add to their watch list.
     * set the ButtonClicked into true to express the button is clicked
     */
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

    /**
     * This function removes a car from the user's watch list and updates the server using a POST
     * request, this function is used only for watch list page
     * @param car_id_pass - The ID of the car that needs to be removed from the user's watch list (the back-end side).
     * execute a function name: onRemoveCard passed from parent component 
     * (this function remove the card/post in client-side front-end )
     * set the ButtonClicked into true to express the button is clicked 
     */
    function remove_to_watchList(car_id_pass){
        props.onRemoveCard(car_id_pass);
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

    /**
     * This function removes a car from the user's watch list and updates the server using a POST
     * request, this function is used only for other pages: index, category
     * @param car_id_pass - The ID of the car that needs to be removed from the user's watch list (the back-end side).
     * set the ButtonClicked into true to express the button is clicked 
     */
    function remove_to_not_watchList(car_id_pass){
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

    /* Everytime buttonClicked is updated to true (Additional logic or actions after button click)
     * execute the function: fetchWatchListData, passed from the parent component 
     * It has function to fetch the watlist data in the backend database
     * Reset buttonClicked state after re-render
     */
    React.useEffect(() => {    
        // Additional logic or actions after button click
        props.fetchWatchListData(); // Fetch updated watch list data
        setButtonClicked(false); // Reset buttonClicked state after re-render 
        }, [buttonClicked]);

    return (
        <React.Fragment>
            {/* Conditional checking @param: checkState passed from the parent 
              * checkState == true, means already added to the watch list  
              * checkState == false, means not add to the watch list yet
            */}
            {/* Conditional checking @param: isWatchListPage passed from the parent 
              * isWatchListPage == true, means the parent is in watch list page
              * isWatchListPage == false, means the parent is in other pages: home, category
            */}
            {props.checkState ? 
                (
                    isWatchListPage ? 
                    (
                        <button 
                            class="btn btn-default w-100 mb-md-0 mb-3 mr-md-3 mr-0" 
                            onClick={() => remove_to_watchList(props.car_id)}>
                            <i class='fas fa-check'></i> 
                            Already added to watch list
                        </button>) 
                    :
                    (
                        <button 
                            class="btn btn-default w-100 mb-md-0 mb-3 mr-md-3 mr-0" 
                            onClick={() => remove_to_not_watchList(props.car_id)}>
                            <i class='fas fa-check'></i> 
                            Already added to watch list
                        </button>
                    )
                )
                :
                (
                    <button 
                        class="btn btn-default w-100 mb-md-0 mb-3 mr-md-3 mr-0" 
                        onClick={() => add_to_watchList(props.car_id)}>
                        <i class='fas fa-plus'></i> 
                        Add to watch list
                    </button>
                )
            }
        </React.Fragment>
    );
  }

