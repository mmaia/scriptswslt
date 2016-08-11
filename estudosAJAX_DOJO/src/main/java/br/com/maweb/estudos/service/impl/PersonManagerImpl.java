package br.com.maweb.estudos.service.impl;

import br.com.maweb.estudos.dao.PersonDao;
import br.com.maweb.estudos.model.Person;
import br.com.maweb.estudos.service.PersonManager;
import br.com.maweb.estudos.service.impl.GenericManagerImpl;

import java.util.List;
import javax.jws.WebService;

@WebService(serviceName = "PersonService", endpointInterface = "br.com.maweb.estudos.service.PersonManager")
public class PersonManagerImpl extends GenericManagerImpl<Person, Long> implements PersonManager {
    PersonDao personDao;

    public PersonManagerImpl(PersonDao personDao) {
        super(personDao);
        this.personDao = personDao;
    }
}