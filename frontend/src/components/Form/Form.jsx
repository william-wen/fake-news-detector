import React from 'react'; 
import 'font-awesome/css/font-awesome.min.css';

class Form extends React.Component{
    state = {
        loading:'none',
        url: '',
        display:'none',
        message:'',
        title:'',
        prediction:''
    }

    handleChange = event => {
        this.setState({url:event.target.value});
    }

    handleSubmit = event => {
        this.setState({loading:'block'})
        fetch('/parse_url', {
            method: 'POST',
            body: JSON.stringify({"url":this.state.url}),
        }).then(res => res.json())
            .then(data => {
                this.setState({
                    loading:'none',
                    display:'block',
                    message: data.message,
                    title:data.title,
                    prediction:data.prediction
                });
            })
            .catch(err => console.log("Error:", err));
        event.preventDefault();
    }

    render(){
        const {loading} = this.state.loading;
        return (
            <div>
                <form onSubmit={this.handleSubmit}>
                    <label>Input the news article link here: <br/></label>
                    <input id="input-url" placeholder="Paste your article link here" value={this.state.url} onChange={this.handleChange} />
                    <input type="submit" value="Submit" />  
                    {/* <button className="button" disabled={!loading}> */}
                    <div style={{display:this.state.loading}}><i className="fa fa-refresh fa-spin" />   Loading...</div>
                    {/* </button>           */}
                </form>
                <div id="article_render" style={{display: this.state.display}}>
                    <p>The title of your article:</p>
                    <div id="article_title" >{this.state.title}</div>
                    <p>Your article</p>
                    <textarea id="article_text" rows="30" cols="70" readOnly value = {this.state.message} />
                    <div>The result of the ML detection:</div>
                    <div id="result">{this.state.prediction}</div>
                </div>
            </div>
        )
    }
}

export default Form;