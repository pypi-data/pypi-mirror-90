# Testing

from rwth_nb.misc.submission import Submission

#os.environ['JUPYTERHUB_API_TOKEN'] = 'xxx'

if __name__ == '__main__':
    sub = Submission('test_realm')

    is_submitted = sub.is_submitted()
    if is_submitted:
        print('Evaluation already submitted')
    else:
        sub.submit({
            'test': [1, 2, 3]
        })

    print('All submissions:')
    for s in sub.get_all():
        print(s)
