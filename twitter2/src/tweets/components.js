import React, {useEffect, useState} from "react";

import {TweetCreate} from './create';
import {loadTweets} from "./lookup";
import {TweetsList} from './list';


export function TweetsComponent(props) {
    const [newTweets, setNewTweets] = useState([])
    const canTweet = props.canTweet === "false" ? false : true
    const handleNewTweet = (newTweet) =>{
      let tempNewTweets = [...newTweets]
      tempNewTweets.unshift(newTweet)
      setNewTweets(tempNewTweets)
    }
    return <div className={props.className}>
            {canTweet === true && <TweetCreate didTweet={handleNewTweet} className='col-12 mb-3' />}
          <TweetsList newTweets={newTweets} {...props} />
    </div>
}


export function TweetList(props) {
    const [tweetsInit, setTweetsInit] = useState([]);
    const [tweets, setTweets] = useState([]);
    // setTweetsInit([...props.newTweets].concat(tweetsInit))
    useEffect(() => {
        const final = [...props.newTweets].concat(tweetsInit)
        if (final.length !== tweets.length) {
            setTweets(final)
        }
    }, [props.newTweets, tweetsInit])

    useEffect(() => {
        const myCallBack = (response, status) => {
            if (status === 200) {
                setTweetsInit(response)
            } else {
                alert("There was an error")
            }
        }
        loadTweets(myCallBack)
    }, [])
    return tweets.map((item, index) => {
        return <Tweet tweet={item} className="my-5 py-5 border bg-white text-dark" key={`${index}-{item.id}`} />
    })
}


export function Tweet(props) {
    const {tweet} = props;
    const className = props.className ? props.className : 'col-10 mx-auto col-md-6';
    const display = action.type === 'like' ? `${tweet.likes} ${action.display}` : action.display;
    
    return <div className={className}>
        <p>{tweet.id} - {tweet.content}</p>
        <div className="btn btn-group">
            <ActionBtn tweet={tweet} action={{type: "like", display: "Likes"}}/>
            <ActionBtn tweet={tweet} action={{type: "unlike", display: "Unlike"}}/>
            <ActionBtn tweet={tweet} action={{type: "retweet", display: "Retweet"}}/>
        </div>
    </div>
}


export function TweetDetailComponent(props){
  const {tweetId} = props
  const [didLookup, setDidLookup] = useState(false)
  const [tweet, setTweet] = useState(null)

  const handleBackendLookup = (response, status) => {
    if (status === 200) {
      setTweet(response)
    } else {
      alert("There was an error finding your tweet.")
    }
  }
  useEffect(()=>{
    if (didLookup === false){

      apiTweetDetail(tweetId, handleBackendLookup)
      setDidLookup(true)
    }
  }, [tweetId, didLookup, setDidLookup])

  return tweet === null ? null : <Tweet tweet={tweet} className={props.className} />
 }