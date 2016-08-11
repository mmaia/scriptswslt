package br.com.maweb.estudos.model;

import java.io.Serializable;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;

import br.com.maweb.estudos.model.BaseObject;
import org.apache.commons.lang.builder.EqualsBuilder;
import org.apache.commons.lang.builder.HashCodeBuilder;
import org.apache.commons.lang.builder.ToStringBuilder;

@Entity
@Table(name="person")
public class Person extends BaseObject implements Serializable{
	private Long id;
	private String firstName;
	private String lastName;
	
	@Id @GeneratedValue(strategy=GenerationType.AUTO)
	public Long getId() {
		return id;
	}
	
	@Column
	public String getFirstName() {
		return firstName;
	}
	
	@Column
	public String getLastName() {
		return lastName;
	}
	public void setId(Long id) {
		this.id = id;
	}
	public void setFirstName(String firstName) {
		this.firstName = firstName;
	}
	public void setLastName(String lastName) {
		this.lastName = lastName;
	}

	/**
	 * @see java.lang.Object#equals(Object)
	 */
	public boolean equals(Object object) {
		if (!(object instanceof Person)) {
			return false;
		}
		Person rhs = (Person) object;
		return new EqualsBuilder().append(
				this.firstName, rhs.firstName).append(this.id, rhs.id).append(
				this.lastName, rhs.lastName).isEquals();
	}

	/**
	 * @see java.lang.Object#hashCode()
	 */
	public int hashCode() {
		return new HashCodeBuilder(571482209, 896330399).append(this.firstName).append(this.id)
				.append(this.lastName).toHashCode();
	}

	/**
	 * @see java.lang.Object#toString()
	 */
	public String toString() {
		return new ToStringBuilder(this).append("lastName", this.lastName)
				.append("id", this.id).append("firstName", this.firstName)
				.toString();
	}
}
