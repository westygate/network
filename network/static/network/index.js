document.addEventListener('DOMContentLoaded', function() {
        
    if (document.querySelector("#new-post-href") != null) {
        document.querySelector("#new-post-href").addEventListener('click', new_post);
    }
    if (document.querySelector("#following-posts-href") != null) {
        document.querySelector("#following-posts-href").addEventListener('click', () =>
                                                                         posts_view("following", 1));
    }
    
    document.querySelector("#all-posts-href").addEventListener('click', () =>
            posts_view("all", 1));
    
    document.querySelector("#new-post-button").addEventListener('click', send_post);
    
    posts_view("all", 1);
});

function createElement(tag, class_name, append_to, value) {
    var element = document.createElement(tag);
    element.setAttribute("class", class_name);
    append_to.append(element);
    element.innerHTML=value;
    return element;
}

function all_posts_view(posts, user, all_posts_container) {
    
    while (all_posts_container.firstChild) {
            all_posts_container.removeChild(all_posts_container.lastChild);

    }
    posts.forEach(post => {
        var container = createElement('div', "one-post-container", all_posts_container, '');         
        var owner = createElement('h5', "one-post-owner", container , post.owner.username);
        owner.addEventListener('click', () => user_profile(post.owner.id));   
        if (post.owner.id == user) {
            var edit = createElement('button', "one-post-edit-button", container , "Edit");
            edit.addEventListener('click', () => edit_post(post));
        }            
        var text = createElement('div', "one-post-text", container , post.text);                
        var timestamp = createElement('div', "one-post-timestamp", container , post.timestamp);
        var likes_container = createElement('div', "one-post-likes-container", container , '');   
        var like_button = createElement('button', "one-post-like-button", likes_container , '');
        var listener;
        if (post.like_users.some(item => item.id === user))
        {
            like_button.innerHTML="Unlike";
            like_button.addEventListener('click', () =>
                                         like_post(post.id, likes, like_button, false),
                                         {once: true});
        }
        else
        {
            like_button.innerHTML="Like";
            like_button.addEventListener('click', () =>
                                         like_post(post.id, likes, like_button, true),
                                         {once: true});
        }
        var likes = createElement('div', "one-post-likes", likes_container , post.likes); 
    });    
    
}

function enable(button, button_link) {

    button.removeAttribute("class");
    button.setAttribute("class", "page-item");
    
    button_link.removeAttribute("tabindex");
    button_link.removeAttribute("aria-disabled");
}

function disable(button, button_link) {

    button.removeAttribute("class");
    button.setAttribute("class", "page-item disabled");
 
    button_link.setAttribute("tabindex", "-1");
    button_link.setAttribute("aria-disabled", "true");
}

function posts_view(category, page) {
    document.querySelector("#view-posts").style.display="block";
    document.querySelector("#edit-post-section").style.display="none";
    document.querySelector("#new-post-section").style.display="none";
    document.querySelector("#user-profile-section").style.display="none";
    
    fetch(`/posts/${category}/${page}`)
    .then(response => response.json())
    .then(result => {
        console.log(result);
        
        var old_button = document.querySelector("#previous-item");
        var previous_button = old_button.cloneNode(true);
        old_button.parentNode.replaceChild(previous_button, old_button);
        var previous =  document.querySelector("#previous");
        if (page === 1) {
            disable(previous_button, previous);
            previous_button.removeEventListener('click',() => posts_view(category, page-1));
        }
        else {
            enable(previous_button, previous);
            previous_button.addEventListener('click',() => posts_view(category, page-1));
        }
        
        old_button = document.querySelector("#next-item");
        var next_button = old_button.cloneNode(true);
        old_button.parentNode.replaceChild(next_button, old_button);
        var next =  document.querySelector("#next");
        if (page === result.page_count) {
            disable(next_button, next);
            next_button.removeEventListener('click',() => posts_view(category, page+1));
        }
        else {
            enable(next_button, next);
            next_button.addEventListener('click',() => posts_view(category, page+1));
        }
        
        all_posts_view(result.posts, result.user, document.querySelector("#posts-section"));   
    });
}

function new_post() {
    document.querySelector("#user-profile-section").style.display="none";
    document.querySelector("#view-posts").style.display="none";
    document.querySelector("#edit-post-section").style.display="none";
    document.querySelector("#new-post-section").style.display="block";
    document.querySelector("#new-post-textarea").value='';
}

function send_post() {
    var text_data = document.querySelector("#new-post-textarea").value;
    fetch('/new_post', {
        method: 'POST',
        body: JSON.stringify({
                text: text_data,
            })
    })
    .then(response => response.json())
    .then(result => {
        console.log( result);
    })
    .catch((error) => {
        console.error(error);
    });
}

function edit_post(post) {
    document.querySelector("#user-profile-section").style.display="none";
    document.querySelector("#view-posts").style.display="none";
    document.querySelector("#new-post-section").style.display="none";
    document.querySelector("#edit-post-section").style.display="block";
    document.querySelector("#edit-post-textarea").value=post.text;
    document.querySelector("#edit-post-button").addEventListener('click', () => update_post(post.id));
}

function update_post(id) {
    var text_data = document.querySelector("#edit-post-textarea").value;
    fetch(`/post/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            text: text_data
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
    })
    .finally(() => {
        user_profile(id);
    });
}

function user_profile(id) {
    document.querySelector("#user-profile-section").style.display="block";
    document.querySelector("#view-posts").style.display="none";
    document.querySelector("#new-post-section").style.display="none";
    document.querySelector("#edit-post-section").style.display="none";
     fetch(`/user/${id}`)
    .then(response => response.json())
    .then(user => {
        console.log(user);
        document.querySelector("#username").innerHTML=user.profile.username;
        var follow_button = document.querySelector("#user-follow-button");
        switch (user.follow) {
            case "none":
                follow_button.style.display="none";
                break;
            case "unfollow":
                follow_button.innerHTML="Unfollow";
                follow_button.style.display="block";
                break;
            case "follow":
                follow_button.innerHTML="Follow";
                follow_button.style.display="block";
                break;
        }

        follow_button.addEventListener('click',() => follow_user(user.follow, user.profile.id));
  
        var followers_section = document.querySelector("#user-followers-section");
        while (followers_section.firstChild) {
        followers_section.removeChild(followers_section.lastChild);
        }
        user.profile.followers.forEach(follower => {
            var follower_name = createElement('div', 'follower-name', followers_section, follower.username);
        });
        var container = document.querySelector("#user-posts-section");
        all_posts_view(user.profile.posts, user.current_user, container);
    
        
    });
    
}

function follow_user(follow, id) {
    fetch(`follow/${id}`, {
        method: "PUT",
        body: JSON.stringify({
            follow: follow
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
    })
    .finally(() => {
        user_profile(id);
    });
}


function like_post(id, likes_view, likes_button, action) {
    fetch(`like/${id}`, {
        method: "PUT",
        body: JSON.stringify({
            like: action
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
        if (result.message == "Post liked") {
            likes_view.innerHTML = parseInt(likes_view.innerHTML) + 1;
            likes_button.innerHTML = "Unlike";
            likes_button.addEventListener('click', () =>
                                         like_post(id, likes_view, likes_button, false),
                                         {once: true});
        }
        if (result.message == "Post unliked") {
            likes_view.innerHTML = parseInt(likes_view.innerHTML) - 1;
            likes_button.innerHTML = "Like";
            likes_button.addEventListener('click', () =>
                                         like_post(id, likes_view, likes_button, true),
                                         {once: true});
        }
    });
}