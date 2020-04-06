import React from 'react'; 

class Form extends React.Component{
    constructor(props){
        super(props);
        this.state = {url: ''};
    }

    handleChange = event => {
        this.setState({url:event.target.value});
    }

    handleSubmit = event => {
        fetch('/parse_url', {
            method: 'POST',
            body: JSON.stringify(this.state),
        }).then(res => res.json())
            .then(data => {
                document.getElementById("article_text").value = data.message;
            })
            .catch(err => console.log("Error:", err));
        event.preventDefault();
    }

    render(){
        return (
            <div>
                <form onSubmit={this.handleSubmit}>
                    <label>Input the news article link here: <br/></label>
                    <input id="input-url" placeholder="Paste your article link here" value={this.state.url} onChange={this.handleChange} />
                    <input type="submit" value="Submit" />            
                </form>
                <p>Your article</p>
                <textarea id="article_text" rows="10" cols="50" />
            </div>
        )
    }
}

export default Form;