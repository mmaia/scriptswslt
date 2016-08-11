package br.com.maweb.estudos.dao;

import br.com.maweb.estudos.dao.GenericDao;

import br.com.maweb.estudos.model.Person;

/**
 * An interface that provides a data management interface to the Person table.
 */
public interface PersonDao extends GenericDao<Person, Long> {

}