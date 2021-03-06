package br.com.maweb.estudos.webapp.action;

import com.opensymphony.xwork2.ActionSupport;
import org.apache.struts2.ServletActionContext;
import br.com.maweb.estudos.service.PersonManager;
import br.com.maweb.estudos.model.Person;
import br.com.maweb.estudos.webapp.action.BaseActionTestCase;
import org.springframework.mock.web.MockHttpServletRequest;

public class PersonActionTest extends BaseActionTestCase {
    private PersonAction action;

    @Override @SuppressWarnings("unchecked")
    protected void onSetUpBeforeTransaction() throws Exception {
        super.onSetUpBeforeTransaction();
        action = new PersonAction();
        PersonManager personManager = (PersonManager) applicationContext.getBean("personManager");
        action.setPersonManager(personManager);
    
        // add a test person to the database
        Person person = new Person();

        // enter all required fields

        personManager.save(person);
    }

    public void testSearch() throws Exception {
        assertEquals(action.list(), ActionSupport.SUCCESS);
        assertTrue(action.getPersons().size() >= 1);
    }

    public void testEdit() throws Exception {
        log.debug("testing edit...");
        action.setId(-1L);
        assertNull(action.getPerson());
        assertEquals("success", action.edit());
        assertNotNull(action.getPerson());
        assertFalse(action.hasActionErrors());
    }

    public void testSave() throws Exception {
        MockHttpServletRequest request = new MockHttpServletRequest();
        ServletActionContext.setRequest(request);
        action.setId(-1L);
        assertEquals("success", action.edit());
        assertNotNull(action.getPerson());

        Person person = action.getPerson();
        // update required fields

        action.setPerson(person);

        assertEquals("input", action.save());
        assertFalse(action.hasActionErrors());
        assertFalse(action.hasFieldErrors());
        assertNotNull(request.getSession().getAttribute("messages"));
    }

    public void testRemove() throws Exception {
        MockHttpServletRequest request = new MockHttpServletRequest();
        ServletActionContext.setRequest(request);
        action.setDelete("");
        Person person = new Person();
        person.setId(-2L);
        action.setPerson(person);
        assertEquals("success", action.delete());
        assertNotNull(request.getSession().getAttribute("messages"));
    }
}