import { Component, OnInit } from '@angular/core';
import { NotifierService } from 'angular-notifier';
import { IBook } from 'src/app/models/book';
import { TypeTag } from 'src/app/models/typeTag';
import { GutenburgAPIService } from 'src/app/services/gutenburg-api.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent implements OnInit {
  data: IBook[] = [];
  suggestions: IBook[] = [];

  errorMessage = 'Indexation en cours au niveau du backend';
  isError = false;

  isSorted = false;
  sortedtype = '';

  constructor(
    private api: GutenburgAPIService,
    private notifier: NotifierService
  ) {}

  ngOnInit(): void {
    // this.api.getAll().then((response) => {
    //   this.data = response.result;
    // });
  }

  onSearch(word): any {
    this.isSorted = false;
    this.api.searchOnApi(word.search).then((response) => {
      console.log(response);
      this.data = response.result.books;
      this.suggestions = response.result.suggestions;
      this.notifier.notify('success', 'Recherche réussie');
    }, (err) => {
      console.log(err);
    });
  }

  onSorted(type: string): any {
    this.isSorted = true;
    this.sortedtype =  type;
    switch (type) {
      case 'pertinence':
        this.data.sort((book1, book2) => {
          if (book1.crank < book2.crank ) { return -1; }
          else if (book1.crank > book2.crank ) { return 1; }
          else { return 0; }
        });
        break;

      case 'langue':
        this.data.sort((book1, book2) => {
          if (book1.language < book2.language ) { return -1; }
          else if (book1.language > book2.language ) { return 1; }
          else { return 0; }
        });
        break;

      case 'author':
        this.data.sort((book1, book2) => {
          if (book1.author < book2.author ) { return -1; }
          else if (book1.author > book2.author ) { return 1; }
          else { return 0; }
        });
        break;

      default:
        break;
    }

  }

}
