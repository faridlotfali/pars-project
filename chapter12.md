#  روز دوازدهم

### <center> ایجاد ماژول کامنت گذاری با angular </center>
```
<app-header></app-header>
<app-home></app-home>
```


```
import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { IComment } from '../comment';
import { viewClassName } from '@angular/compiler';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  comments : IComment [] = [];

  @ViewChild('commentText') conn : ElementRef;

  constructor() { }

  ngOnInit() {
  }

  commentLike(c:IComment){
    c.like++;
  }

  commentDislike(c:IComment){
    c.dislike--;
  }

  reviewsCount(c:IComment , n: HTMLInputElement){
    c.numberOfReviews++;
    c.star += parseInt(n.value)
  }
  addComment(){
    let c : IComment ={
      comment: this.conn.nativeElement.value, 
      dislike : 0,
      like : 0,
      numberOfReviews : 0,
      star : 0,
    }
    this.comments.push(c);
  }
}
```


```
<div style="width: 400px; margin: 2em; ">
  <label for="comment">Comment</label>
  <textarea #commentText name="comment" class="form-control"></textarea>
  <button (click)="addComment()" class="btn btn-primary mt-2 "> Add Comment</button>
</div>

<div style="width: 400px; margin: 2em;" *ngIf = "comments != null">
  <div *ngFor="let c of comments">
    <p style="clear: both;">{{c.comment}}</p>
    <div style="float: left;">
        <app-star [rating] = "c.numberOfReviews != 0 ? c.star/c.numberOfReviews : 0"></app-star>
    </div>
    <div style="float: right;">
      <span>{{c.like}}</span>
      <li (click) = "commentLike(c)" class="fa fa-heart" style="cursor: pointer;"></li>
      <span>{{c.dislike}}</span>
      <li (click) = "commentDislike(c)" class="fa fa-heart-o" style="cursor: pointer;"></li>
    </div>
    <div style="clear: both;">
      <span>Rating: </span>
      <input #ratingInput (keyup.enter) = "reviewsCount(c , ratingInput)"  type="number" min=0 max=5 style="background-color: #333; color: white; width: 30px;">
      <hr>
      <br>
    </div>
  </div>
</div>
```

```
<nav class="navbar navbar-expand-lg ">
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarTogglerDemo03" aria-controls="navbarTogglerDemo03" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <a class="navbar-brand" href="#">Survey</a>

  <div class="collapse navbar-collapse" id="navbarTogglerDemo03">
    <ul class="navbar-nav mr-auto mt-2 mt-lg-0">
      <li class="nav-item active">
        <a class="nav-link" href="#">Home <span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#">Link</a>
      </li>
      <li class="nav-item">
        <a class="nav-link disabled" href="#">Disabled</a>
      </li>
    </ul>
    <form class="form-inline my-2 my-lg-0">
      <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search">
      <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
    </form>
  </div>
</nav>
```