package br.com.maweb.estudos.dao;

import br.com.maweb.estudos.dao.BaseDaoTestCase;
import br.com.maweb.estudos.model.Person;
import org.springframework.dao.DataAccessException;

import java.util.List;

public class PersonDaoTest extends BaseDaoTestCase {
    private PersonDao personDao;

    public void setPersonDao(PersonDao personDao) {
        this.personDao = personDao;
    }

    public void testAddAndRemovePerson() throws Exception {
        Person person = new Person();

        // enter all required fields

        log.debug("adding person...");
        person = personDao.save(person);

        person = personDao.get(person.getId());

        assertNotNull(person.getId());

        log.debug("removing person...");

        personDao.remove(person.getId());

        try {
            personDao.get(person.getId());
            fail("Person found in database");
        } catch (DataAccessException e) {
            log.debug("Expected exception: " + e.getMessage());
            assertNotNull(e);
        }
    }
}