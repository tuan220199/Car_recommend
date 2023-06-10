'use strict';

const e = React.createElement;

function Pagination(props){

    // Create the previous and next page of the current page with React.useState
    // props.pageNumber is the parameter passed from the parent 
    const [prevPage, setprevPage] = React.useState(props.pageNumber-1);
    const [nextPage, setNextPage] = React.useState(+props.pageNumber+1);

    // Re-render/ Update the value of previous and next page when the currrent page is updated
    React.useEffect(() => {
      setprevPage(props.pageNumber-1);
      setNextPage(+props.pageNumber+1);
    }, [props.pageNumber]);

    return (
        <div id="pagination">
            <nav aria-label="Page navigation example">
                <ul className="pagination justify-content-center">
                {prevPage > 0 && (
                    <React.Fragment>
                    <li className="page-item">
                        <button onClick={()=> props.onPageChange(prevPage)}>
                        <span aria-hidden="true">&laquo;</span>
                        </button>
                    </li>
                    <li className="page-item">
                        <button onClick={()=> props.onPageChange(prevPage)}>
                        {prevPage}
                        </button>
                    </li>
                    </React.Fragment>
                )}
                <li className="page-item">
                    <button onClick={() => props.onPageChange(props.pageNumber)}>
                    {props.pageNumber}
                    </button>
                </li>
                {nextPage < props.numberPages + 1 && (
                    <React.Fragment>
                    <li className="page-item">
                        <button onClick={()=> props.onPageChange(nextPage)}>
                        {nextPage}
                        </button>
                    </li>
                    <li className="page-item">
                        <button onClick={()=> props.onPageChange(nextPage)}>
                        <span aria-hidden="true">&raquo;</span>
                        </button>
                    </li>
                    </React.Fragment>
                )}
                </ul>
            </nav>
        </div>
    );    
}
