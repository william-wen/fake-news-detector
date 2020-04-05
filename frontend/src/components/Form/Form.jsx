import React from 'react'; 
import axios from 'axios';

class Form extends React.Component{
    constructor(props){
        super(props);
        this.state = {url: ''};
    }

    handleChange = event => {
        this.setState({url:event.target.value});
    }

    handleSubmit = event => {
        fetch('/verify', {
            method: 'POST',
            body: JSON.stringify(this.state),
        }).then(res => res.json())
            .then(data => console.log(data))
            .catch(err => console.error("Error:", err));
        event.preventDefault();
    }

    render(){
        return (
            <form onSubmit={this.handleSubmit}>
                <label>Input the news article link here: <br/></label>
                <input id="input-url" placeholder="Paste your article link here" value={this.state.url} onChange={this.handleChange} />
                <input type="submit" value="Submit" />            
            </form>
        )
    }
}

export default Form;