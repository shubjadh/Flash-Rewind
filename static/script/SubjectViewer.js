function SubjectViewer(mySubjects, numRows, subjectsPerRow) {
    const SUBJECTS_PER_PAGE = numRows * subjectsPerRow;

    this.updateCards = (subjects) => {
        $('#cards').empty();
        
        console.log(subjects);
        console.log(subjects.length);
        total_subjects = subjects.length;
        needed_rows = Math.ceil(total_subjects/subjectsPerRow);
        console.log(needed_rows);
        needed_columns = total_subjects;
        for (let row = 0; row < needed_rows; row++) {
            const deck = $('<div class="card-deck"></div>');
            col_length = needed_columns < subjectsPerRow ? needed_columns : subjectsPerRow;

            for (let col = 0; col < col_length; col++) {
                const index = row * subjectsPerRow + col;
                if (index < subjects.length) {
                    const subject = subjects[row * subjectsPerRow + col];

                    const card = $(`
                        <div class="card col-4">
                            <div class="card-body">
                                <h5 class="card-title">${subject.subjectName}</h5>
                                <p   class="card-text ">${subject.description}</p>
                                <button class="revise-button btn btn-primary"> Revise</button>
                                <a class="edit-button btn btn-primary" href="subject/${subject.subjectId}/notes/"> Edit</a>
                                <button class="delete-button btn btn-primary"> Delete</button>

                            </div>
                        </div>
                    `);

                    $(card).find('.delete-button').on('click', _ => {
                        console.log(subject.subjectId);
                        this.remove(subject.subjectId);
                    });
                    
                    $(card).find('.revise-button').on('click', _ => {
                        console.log(subject.subjectId);
                        window.location.href = '/flash_cards/' + subject.subjectId;
                    });

                    $(deck).append(card);
                } else {

                    const card = $(`
                        <div class="card">
                        </div>
                    `);
                    $(deck).append(card);

                }
            }
            needed_columns = needed_columns - subjectsPerRow;

            $('#cards').append(deck);
        }
    }

    const createPageLink = (text, toPage, active, disabled) => {
        const link = $(`
            <li class="page-item">
                <a class="page-link">${text}</a>
            </li>
        `);
        $(link).find('.page-link').on('click', _ => {
            this.currentPage = toPage;
            this.load();
        });
        if (active)
            link.addClass('active');
        if (disabled)
            link.addClass('disabled');
        return link;
    }

    this.currentPage = 1;

    this.updatePagination = (total) => {
        let pages = Math.ceil(total / SUBJECTS_PER_PAGE);
        $('#paginator').empty().append(
            createPageLink('Previous', this.currentPage - 1, false, this.currentPage == 1)
        );
        for (let page = 1; page <= pages; page++)
            $('#paginator').append(
                createPageLink(page, page, page == this.currentPage, false)
            );
        $('#paginator').append(
            createPageLink('Next', this.currentPage + 1, false, this.currentPage == pages)
        );
    }

    this.update = (data) => {
        this.updateCards(data.subjects);
        this.updatePagination(data.total);
    }

    this.load = () => {
        console.log("inside load");
        $.get('/api/user/subjects', {
            n: SUBJECTS_PER_PAGE,
            offset: (this.currentPage - 1) * SUBJECTS_PER_PAGE
        }, (data) => {
            this.update(data);
        });
    }

    this.remove = (subject_id) => {
        console.log("inside delete");
        $.ajax({
            url: `/api/user/subjects/${subject_id}`,
            type: 'DELETE',
            success: (data) => {
              console.log(`subject with id ${subject_id} deleted successfully`);
            },
            error: (xhr, status, error) => {
              console.error(`failed to delete subject with id ${subject_id}: ${error}`);
            }
        });
        this.load(true, 3, 3);
    }

    

   
    
}
