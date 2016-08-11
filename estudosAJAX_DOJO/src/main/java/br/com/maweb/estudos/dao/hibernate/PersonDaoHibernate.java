package br.com.maweb.estudos.dao.hibernate;

import br.com.maweb.estudos.model.Person;
import br.com.maweb.estudos.dao.PersonDao;
import br.com.maweb.estudos.dao.hibernate.GenericDaoHibernate;

public class PersonDaoHibernate extends GenericDaoHibernate<Person, Long> implements PersonDao {

    public PersonDaoHibernate() {
        super(Person.class);
    }
}
